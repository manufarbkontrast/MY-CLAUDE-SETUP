---
name: browser-automation-claude
description: Automate browsers with Claude Vision using Playwright. DOM-aware targeting, coordinate scaling, sampling loops. Use when building browser automation, web scraping, or UI testing with Claude.
version: 1.0.0
license: MIT
metadata:
  last_verified: 2025-02-14
  keywords:
    - browser
    - playwright
    - vision
    - dom
    - automation
    - web-scraping
  related_skills:
    - claude-agent-loop
    - autonomous-coding-agent
    - playwright
---

# Browser Automation with Claude

Automate web browsers using Claude's vision capabilities and Playwright. This skill covers DOM-aware element targeting, coordinate scaling between Claude's vision resolution and the browser viewport, and the sampling loop pattern for running Claude in agentic browser sessions.

Based on Anthropic's [browser-use-demo](https://github.com/anthropics/claude-quickstarts/tree/main/browser-use-demo) reference implementation.

## Quick Start

Minimal browser session with Claude controlling Playwright:

```python
import asyncio
import base64
from anthropic import Anthropic
from playwright.async_api import async_playwright

SYSTEM_PROMPT = """You control a Chromium browser via Playwright.
After navigating, call read_page to get element refs before interacting.
Use refs (ref_1, ref_2) for reliable targeting over coordinates.
Use get_page_text to read content instead of screenshots."""

async def run_browser_task(task: str):
    client = Anthropic()
    pw = await async_playwright().start()
    browser = await pw.chromium.launch(headless=False)
    page = await (await browser.new_context(
        viewport={"width": 1920, "height": 1080}
    )).new_page()

    await page.goto("https://example.com")
    screenshot_bytes = await page.screenshot()
    image_b64 = base64.b64encode(screenshot_bytes).decode()

    messages = [{"role": "user", "content": [
        {"type": "image", "source": {
            "type": "base64", "media_type": "image/png", "data": image_b64}},
        {"type": "text", "text": task},
    ]}]

    while True:
        response = client.messages.create(
            model="claude-sonnet-4-5-20250514",
            max_tokens=4096,
            system=[{"type": "text", "text": SYSTEM_PROMPT}],
            tools=[BROWSER_TOOL],
            messages=messages,
        )
        if response.stop_reason != "tool_use":
            break
        # ... process tool calls ...

    await browser.close()
    await pw.stop()
```

See `templates/browser-session.py` for the complete runnable version.

## Core Features

- **DOM-aware element targeting** via ref IDs (ref_1, ref_2, ...) instead of brittle pixel coordinates
- **Coordinate scaling** between Claude's vision resolution (1456x819) and browser viewport (1920x1080)
- **Accessibility tree generation** via JavaScript injection for structured page understanding
- **Sampling loop pattern** for running Claude in an agentic loop until task completion
- **Form manipulation** with direct value setting via element references
- **Text extraction** prioritizing article content with fallback to full page body
- **Element finding** using AI-powered semantic search across the DOM tree
- **Screenshot capture** with viewport and zoomed region support

## Resources

### References

| File | Description |
|------|-------------|
| [references/sampling-loop.md](references/sampling-loop.md) | The agentic sampling loop pattern: running Claude in a loop processing tool calls until task completion. Covers response processing, message building, and image management. |
| [references/coordinate-scaling.md](references/coordinate-scaling.md) | Coordinate scaling between Claude Vision's processed resolution and the actual browser viewport. Includes the CoordinateScaler class, scale formulas, and threshold checks. |
| [references/dom-interaction.md](references/dom-interaction.md) | DOM interaction patterns: accessibility tree generation, global element map, ref-based targeting, and JavaScript injection. Why DOM-based interaction beats pixel coordinates. |
| [references/browser-tools.md](references/browser-tools.md) | Complete reference for all browser tool actions: navigation, DOM reading, text extraction, mouse/keyboard actions, form input, screenshots, scrolling, and JavaScript execution. |

### Templates

| File | Description |
|------|-------------|
| [templates/browser-session.py](templates/browser-session.py) | Minimal Playwright browser session with Claude sampling loop. Ready to run with an Anthropic API key. |
| [templates/coordinate-scaler.py](templates/coordinate-scaler.py) | Standalone CoordinateScaler class for mapping Claude vision coordinates to viewport coordinates. Copy-paste ready. |
| [templates/dom-extraction.js](templates/dom-extraction.js) | JavaScript that generates an accessibility tree with ref IDs for Claude to understand page structure. |
| [templates/element-finder.js](templates/element-finder.js) | JavaScript that finds elements by reference ID, scrolls them into view, and returns coordinates and metadata. |
| [templates/form-handler.js](templates/form-handler.js) | JavaScript for form input manipulation: text fields, checkboxes, radio buttons, selects, date/range inputs. |
