"""
Minimal browser automation session with Claude and Playwright.

Usage:
    pip install anthropic playwright
    playwright install chromium
    export ANTHROPIC_API_KEY=your-key
    python browser-session.py
"""

import asyncio
import base64
import json
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path

from anthropic import Anthropic
from playwright.async_api import async_playwright


# --- Configuration ---

VIEWPORT_WIDTH = 1920
VIEWPORT_HEIGHT = 1080
MAX_TOKENS = 4096
MODEL = "claude-sonnet-4-5-20250514"

SYSTEM_PROMPT = f"""<SYSTEM_CAPABILITY>
* You control a Chromium browser via Playwright automation.
* The current date is {datetime.today().strftime("%A, %B %-d, %Y")}.
</SYSTEM_CAPABILITY>

<TOOL_GUIDANCE>
After navigating, call read_page to get element refs before interacting.
Use refs (ref_1, ref_2) for reliable targeting over coordinates.
Use get_page_text to read content instead of screenshots.
If refs fail, fall back to coordinate-based actions.
</TOOL_GUIDANCE>"""

BROWSER_TOOL = {
    "name": "browser",
    "description": "Browser automation tool. Actions: navigate, screenshot, "
    "left_click, type, key, read_page, get_page_text, scroll, form_input, wait.",
    "input_schema": {
        "type": "object",
        "required": ["action"],
        "properties": {
            "action": {
                "type": "string",
                "enum": [
                    "navigate", "screenshot", "left_click", "type",
                    "key", "read_page", "get_page_text", "scroll",
                    "form_input", "wait",
                ],
            },
            "text": {"type": "string"},
            "ref": {"type": "string"},
            "coordinate": {"type": "array", "items": {"type": "integer"}},
            "scroll_direction": {
                "type": "string",
                "enum": ["up", "down", "left", "right"],
            },
            "scroll_amount": {"type": "integer"},
            "duration": {"type": "number"},
            "value": {"type": ["string", "number", "boolean"]},
        },
    },
}


# --- Tool Result ---

@dataclass(frozen=True)
class ToolResult:
    output: str | None = None
    error: str | None = None
    base64_image: str | None = None


# --- Browser Actions ---

async def execute_browser_action(page, action_input: dict) -> ToolResult:
    """Execute a single browser action and return the result."""
    action = action_input["action"]

    if action == "navigate":
        url = action_input.get("text", "")
        if not url.startswith(("http://", "https://")):
            url = f"https://{url}"
        await page.goto(url, wait_until="domcontentloaded")
        await asyncio.sleep(2)
        return await _take_screenshot(page)

    elif action == "screenshot":
        return await _take_screenshot(page)

    elif action == "left_click":
        coord = action_input.get("coordinate")
        if coord:
            x, y = _scale_coordinates(coord[0], coord[1])
            await page.mouse.click(x, y)
            return ToolResult(output=f"Clicked at ({x}, {y})")
        return ToolResult(error="Coordinate required for click")

    elif action == "type":
        text = action_input.get("text", "")
        await page.keyboard.type(text)
        return ToolResult(output=f"Typed: {text}")

    elif action == "key":
        key = action_input.get("text", "")
        await page.keyboard.press(key)
        return ToolResult(output=f"Pressed: {key}")

    elif action == "read_page":
        dom_script = Path(__file__).parent / "dom-extraction.js"
        if dom_script.exists():
            script = dom_script.read_text()
            result = await page.evaluate(
                f"(function() {{ {script} "
                f"return window.__generateAccessibilityTree(''); }})()"
            )
            content = result.get("pageContent", str(result))
            return ToolResult(output=content)
        return ToolResult(error="DOM extraction script not found")

    elif action == "get_page_text":
        text_script = Path(__file__).parent / "dom-extraction.js"
        text = await page.evaluate("document.body.innerText")
        title = await page.evaluate("document.title")
        url = page.url
        return ToolResult(output=f"Title: {title}\nURL: {url}\n---\n{text}")

    elif action == "scroll":
        direction = action_input.get("scroll_direction", "down")
        amount = action_input.get("scroll_amount", 3)
        delta = amount * 100
        if direction == "up":
            await page.evaluate(f"window.scrollBy(0, -{delta})")
        elif direction == "down":
            await page.evaluate(f"window.scrollBy(0, {delta})")
        await asyncio.sleep(0.5)
        return await _take_screenshot(page)

    elif action == "form_input":
        ref = action_input.get("ref")
        value = action_input.get("value")
        if not ref or value is None:
            return ToolResult(error="ref and value required for form_input")
        # Simplified: use evaluate to set value
        result = await page.evaluate(
            f"""(() => {{
                const weakRef = window.__claudeElementMap && window.__claudeElementMap['{ref}'];
                if (!weakRef) return {{ success: false, message: 'Ref not found' }};
                const el = weakRef.deref();
                if (!el) return {{ success: false, message: 'Element gone' }};
                el.value = {json.dumps(value)};
                el.dispatchEvent(new Event('input', {{ bubbles: true }}));
                el.dispatchEvent(new Event('change', {{ bubbles: true }}));
                return {{ success: true }};
            }})()"""
        )
        if result.get("success"):
            return ToolResult(output=f"Set {ref} to {value}")
        return ToolResult(error=result.get("message", "Failed"))

    elif action == "wait":
        duration = action_input.get("duration", 1.0)
        await asyncio.sleep(duration)
        return ToolResult(output=f"Waited {duration}s")

    return ToolResult(error=f"Unknown action: {action}")


async def _take_screenshot(page) -> ToolResult:
    screenshot_bytes = await page.screenshot(full_page=False)
    image_b64 = base64.b64encode(screenshot_bytes).decode()
    return ToolResult(base64_image=image_b64)


# Coordinate scaling: Claude Vision 16:9 -> viewport
CLAUDE_WIDTH = 1456
CLAUDE_HEIGHT = 819


def _scale_coordinates(x: int, y: int) -> tuple[int, int]:
    scale_x = VIEWPORT_WIDTH / CLAUDE_WIDTH
    scale_y = VIEWPORT_HEIGHT / CLAUDE_HEIGHT
    if abs(scale_x - 1.0) < 0.05 and abs(scale_y - 1.0) < 0.05:
        return x, y
    if x > CLAUDE_WIDTH * 1.2 or y > CLAUDE_HEIGHT * 1.2:
        return x, y
    return (
        min(int(x * scale_x), VIEWPORT_WIDTH - 1),
        min(int(y * scale_y), VIEWPORT_HEIGHT - 1),
    )


# --- Sampling Loop ---

def build_tool_result_content(result: ToolResult) -> list[dict]:
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
        content.append({"type": "text", "text": f"Error: {result.error}"})
    return content


async def sampling_loop(client: Anthropic, page, task: str):
    """Run Claude in a loop until the browser task is complete."""
    # Take initial screenshot
    screenshot = await _take_screenshot(page)
    messages = [
        {
            "role": "user",
            "content": [
                {
                    "type": "image",
                    "source": {
                        "type": "base64",
                        "media_type": "image/png",
                        "data": screenshot.base64_image,
                    },
                },
                {"type": "text", "text": task},
            ],
        }
    ]

    while True:
        response = client.messages.create(
            model=MODEL,
            max_tokens=MAX_TOKENS,
            system=[{"type": "text", "text": SYSTEM_PROMPT}],
            tools=[BROWSER_TOOL],
            messages=messages,
        )

        # Build assistant content
        assistant_content = []
        tool_uses = []
        for block in response.content:
            if block.type == "text":
                assistant_content.append({"type": "text", "text": block.text})
                print(f"Claude: {block.text}")
            elif block.type == "tool_use":
                tool_use = {
                    "type": "tool_use",
                    "id": block.id,
                    "name": block.name,
                    "input": block.input,
                }
                assistant_content.append(tool_use)
                tool_uses.append(tool_use)
                print(f"Tool: {block.name}({json.dumps(block.input)})")

        messages.append({"role": "assistant", "content": assistant_content})

        if not tool_uses:
            break

        # Execute tools and collect results
        tool_results = []
        for tool_use in tool_uses:
            result = await execute_browser_action(page, tool_use["input"])
            tool_results.append({
                "type": "tool_result",
                "tool_use_id": tool_use["id"],
                "content": build_tool_result_content(result),
            })

        messages.append({"role": "user", "content": tool_results})

    return messages


# --- Main ---

async def main():
    task = input("Enter browser task: ")

    client = Anthropic()
    pw = await async_playwright().start()
    browser = await pw.chromium.launch(
        headless=False,
        args=[f"--window-size={VIEWPORT_WIDTH},{VIEWPORT_HEIGHT}"],
    )
    context = await browser.new_context(
        viewport={"width": VIEWPORT_WIDTH, "height": VIEWPORT_HEIGHT},
    )
    page = await context.new_page()
    await page.goto("about:blank")

    try:
        await sampling_loop(client, page, task)
    finally:
        await browser.close()
        await pw.stop()


if __name__ == "__main__":
    asyncio.run(main())
