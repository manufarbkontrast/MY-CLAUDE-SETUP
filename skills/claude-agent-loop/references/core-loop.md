# Core Agent Loop

## Pattern

The agent loop is an infinite `while True` that continues until Claude responds without any `tool_use` blocks.

```
User Input -> API Call -> Response
                           |
                    Has tool_use? --NO--> Return response (done)
                           |
                          YES
                           |
                    Execute tools
                           |
                    Append tool_results as "user" message
                           |
                    Loop back to API Call
```

## Implementation

```python
async def agent_loop(self, user_input: str):
    await self.history.add_message("user", user_input, None)
    tool_dict = {tool.name: tool for tool in self.tools}

    while True:
        self.history.truncate()  # Prevent context overflow

        response = self.client.messages.create(
            model=self.config.model,
            max_tokens=self.config.max_tokens,
            temperature=self.config.temperature,
            system=self.system,
            messages=self.history.format_for_api(),
            tools=[tool.to_dict() for tool in self.tools],
        )

        # Extract tool calls from response
        tool_calls = [b for b in response.content if b.type == "tool_use"]

        # Store assistant response in history
        await self.history.add_message("assistant", response.content, response.usage)

        if tool_calls:
            # Execute tools and feed results back
            tool_results = await execute_tools(tool_calls, tool_dict)
            await self.history.add_message("user", tool_results)
        else:
            return response  # No tool calls = agent is done
```

## Key Decisions

### Exit Condition
The loop exits when `response.content` contains no `tool_use` blocks. This means Claude has finished its work and is providing a final text response.

### Truncation Before Each Call
`self.history.truncate()` runs before every API call to ensure the message history fits within the context window. This prevents 400 errors from oversized requests.

### Message Ordering
Messages must alternate: user -> assistant -> user -> assistant. Tool results are sent as "user" messages with `type: "tool_result"` blocks, each referencing the `tool_use_id` they respond to.

### Parameter Override Pattern
Allow custom parameters to override defaults using dict unpacking:

```python
def prepare_params(self) -> dict:
    return {
        "model": self.config.model,
        "max_tokens": self.config.max_tokens,
        "system": self.system,
        "messages": self.history.format_for_api(),
        "tools": [tool.to_dict() for tool in self.tools],
        **self.message_params,  # Overrides any of the above
    }
```

## Sync vs Async

The agent supports both modes:

```python
# Async (preferred for MCP and parallel tools)
async def run_async(self, user_input: str):
    async with AsyncExitStack() as stack:
        mcp_tools = await setup_mcp_connections(self.mcp_servers, stack)
        self.tools.extend(mcp_tools)
        return await self.agent_loop(user_input)

# Sync wrapper
def run(self, user_input: str):
    return asyncio.run(self.run_async(user_input))
```

## Verbose Logging

Add optional logging to trace agent behavior:

```python
if self.verbose:
    for block in response.content:
        if block.type == "text":
            print(f"[{self.name}] Output: {block.text}")
        elif block.type == "tool_use":
            params_str = ", ".join(f"{k}={v}" for k, v in block.input.items())
            print(f"[{self.name}] Tool call: {block.name}({params_str})")
```
