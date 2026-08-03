# Sampling Loop Pattern

The sampling loop is the core pattern for running Claude in an agentic browser automation session. Claude receives screenshots and DOM information, decides what actions to take, executes them via tool calls, and continues until the task is complete.

## Overview

The loop follows this cycle:

1. Send messages (including screenshots) to Claude API
2. Receive response with text and/or tool_use blocks
3. If tool_use blocks present: execute tools, collect results, append to messages, repeat
4. If no tool_use blocks: task is complete, return

```
User message (with screenshot)
        |
        v
   Claude API call
        |
        v
   Response processing
        |
        +---> Has tool_use blocks? --YES--> Execute tools
        |                                      |
        |                                      v
        |                              Append results to messages
        |                                      |
        |                                      +----> (loop back to API call)
        |
        +---> No tool_use blocks? ---> Return (task complete)
```

## The Main Loop

The sampling loop continues calling Claude until it stops requesting tool use:

```python
async def sampling_loop(
    client: Anthropic,
    model: str,
    system_prompt: str,
    messages: list[dict],
    tools: list[dict],
    browser_tool: BrowserTool,
    max_tokens: int = 4096,
):
    tool_collection = ToolCollection(browser_tool)

    system = [{"type": "text", "text": system_prompt}]

    while True:
        response = client.messages.create(
            max_tokens=max_tokens,
            messages=messages,
            model=model,
            system=system,
            tools=tool_collection.to_params(),
        )

        # Process the response
        processor = ResponseProcessor()
        processed = processor.process_response(response)

        # Build assistant message (preserves both text and tool_use blocks)
        builder = MessageBuilder()
        builder.add_assistant_message(messages, processed.assistant_content)

        if processed.tool_uses:
            # Execute all tool calls and collect results
            tool_results = await processor.execute_tools(
                processed.tool_uses, tool_collection
            )
            # Add results as a user message
            builder.add_tool_results(messages, tool_results)
            # Loop continues
        else:
            # No tools requested - task is complete
            return messages
```

## Separation of Concerns

The pattern separates response processing from message building into two distinct classes.

### ResponseProcessor

Handles parsing the API response into a structured format:

```python
from dataclasses import dataclass
from typing import Any

@dataclass
class ProcessedResponse:
    assistant_content: list[dict]   # All content blocks (text + tool_use)
    tool_uses: list[dict]           # Just the tool_use blocks
    has_text: bool
    has_tools: bool

class ResponseProcessor:
    def process_response(self, response) -> ProcessedResponse:
        assistant_content = []
        tool_uses = []

        for block in response.content:
            if block.type == "text":
                assistant_content.append({
                    "type": "text", "text": block.text
                })
            elif block.type == "tool_use":
                tool_use = {
                    "type": "tool_use",
                    "id": block.id,
                    "name": block.name,
                    "input": block.input,
                }
                assistant_content.append(tool_use)
                tool_uses.append(tool_use)

        return ProcessedResponse(
            assistant_content=assistant_content,
            tool_uses=tool_uses,
            has_text=any(b.type == "text" for b in response.content),
            has_tools=len(tool_uses) > 0,
        )
```

### MessageBuilder

Handles constructing properly structured messages for the API:

```python
class MessageBuilder:
    def add_assistant_message(self, messages: list, content: list[dict]):
        """Append a complete assistant message preserving text + tool_use."""
        if content:
            messages.append({"role": "assistant", "content": content})

    def add_tool_results(self, messages: list, tool_results: list[dict]):
        """Append tool results as a single user message."""
        if tool_results:
            messages.append({"role": "user", "content": tool_results})
```

Key insight: the assistant message must contain ALL content blocks (text explanations AND tool_use blocks) together. Splitting them into separate messages breaks the conversation structure.

### Tool Execution

Tools are executed and results formatted as tool_result blocks:

```python
async def execute_tools(
    self,
    tool_uses: list[dict],
    tool_collection: ToolCollection,
) -> list[dict]:
    results = []
    for tool_use in tool_uses:
        try:
            tool = tool_collection.tool_map[tool_use["name"]]
            result = await tool(**tool_use["input"])
            results.append(build_tool_result(result, tool_use["id"]))
        except Exception as e:
            results.append({
                "type": "tool_result",
                "tool_use_id": tool_use["id"],
                "is_error": True,
                "content": [{"type": "text", "text": str(e)}],
            })
    return results
```

## Image Management in Messages

Screenshots are sent as base64-encoded images in tool results. Over a long session, accumulated images consume context window space. Filter old images to keep only the N most recent:

```python
def filter_to_n_most_recent_images(
    messages: list[dict],
    images_to_keep: int,
    min_removal_threshold: int = 10,
):
    """Remove old images from messages, keeping only the most recent ones."""
    if images_to_keep <= 0:
        raise ValueError("images_to_keep must be > 0")

    total_images = sum(
        1
        for msg in messages
        if msg["role"] == "user"
        for block in msg.get("content", [])
        if isinstance(block, dict) and block.get("type") == "image"
    )

    images_to_remove = total_images - images_to_keep
    if images_to_remove < min_removal_threshold:
        return

    removed = 0
    for msg in messages:
        if msg["role"] == "user" and isinstance(msg.get("content"), list):
            new_content = []
            for block in msg["content"]:
                if isinstance(block, dict) and block.get("type") == "image":
                    if removed < images_to_remove:
                        removed += 1
                        continue
                new_content.append(block)
            msg["content"] = new_content
```

The `min_removal_threshold` prevents unnecessary processing when there are few images.

## Tool Result Structure

Tool results include text output and optionally a base64 screenshot:

```python
def build_tool_result(result: ToolResult, tool_use_id: str) -> dict:
    content = []

    if result.output:
        content.append({"type": "text", "text": result.output})

    if result.base64_image:
        content.append({
            "type": "image",
            "source": {
                "type": "base64",
                "media_type": "image/png",
                "data": result.base64_image,
            },
        })

    if result.error:
        return {
            "type": "tool_result",
            "tool_use_id": tool_use_id,
            "is_error": True,
            "content": [{"type": "text", "text": f"Error: {result.error}"}],
        }

    return {
        "type": "tool_result",
        "tool_use_id": tool_use_id,
        "content": content,
    }
```

## System Prompt

The system prompt guides Claude on how to use browser tools effectively:

```python
BROWSER_SYSTEM_PROMPT = f"""<SYSTEM_CAPABILITY>
* You control a Chromium browser via Playwright automation.
* The current date is {datetime.today().strftime("%A, %B %-d, %Y")}.
</SYSTEM_CAPABILITY>

<TOOL_GUIDANCE>
You receive a screenshot at the start of each turn. Look at it to see
the current page - if you're already where you need to be, don't
re-navigate.

After navigating to a new page, always call read_page to get element
references (ref_1, ref_2, etc.) before interacting. Use these refs
with interaction tools (click, type, hover, form_input, etc.).

When you need to extract or read text content, always use get_page_text.

If DOM-based actions (refs) aren't working, fall back to screenshot +
coordinate-based actions.
</TOOL_GUIDANCE>

<TIPS>
* Prefer get_page_text over scrolling when looking for information
* Use execute_js for data extraction from JavaScript variables
* Use full URLs with https://
* Use wait for slow-loading pages
* Use scroll_to with a ref to reveal elements
* Use form_input with refs for form fields
* Use key for shortcuts (e.g., "ctrl+a")
* Close popups when they appear
* Verify actions succeeded before moving on
</TIPS>"""
```

## Prompt Caching

For the Anthropic API provider, enable prompt caching to reduce costs on repeated system prompts:

```python
system = {
    "type": "text",
    "text": system_prompt,
    "cache_control": {"type": "ephemeral"},
}
```

This caches the system prompt across API calls within the sampling loop, avoiding re-tokenization on each turn.
