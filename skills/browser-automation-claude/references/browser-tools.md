# Browser Tool Actions Reference

Complete reference for all actions available in the browser automation tool. The tool is registered as `"browser"` and accepts an `action` parameter plus action-specific parameters.

## Tool Definition

```python
BROWSER_TOOL = {
    "name": "browser",
    "description": "A browser automation tool for web interaction.",
    "input_schema": {
        "type": "object",
        "required": ["action"],
        "properties": {
            "action": {"type": "string", "enum": [
                "navigate", "screenshot", "left_click", "right_click",
                "middle_click", "double_click", "triple_click", "hover",
                "left_click_drag", "left_mouse_down", "left_mouse_up",
                "scroll", "scroll_to", "type", "key", "hold_key",
                "read_page", "find", "get_page_text", "wait",
                "form_input", "zoom", "execute_js",
            ]},
            "text": {"type": "string"},
            "ref": {"type": "string"},
            "coordinate": {"type": "array", "items": {"type": "integer"}},
            "start_coordinate": {"type": "array", "items": {"type": "integer"}},
            "scroll_direction": {"type": "string", "enum": ["up", "down", "left", "right"]},
            "scroll_amount": {"type": "integer"},
            "duration": {"type": "number"},
            "value": {"type": ["string", "number", "boolean"]},
            "region": {"type": "array", "items": {"type": "integer"}},
        },
    },
}
```

## Navigation Actions

### navigate

Navigate to a URL or use browser history.

| Parameter | Required | Description |
|---|---|---|
| text | Yes | URL to navigate to, or "back"/"forward" for history |

- Automatically prepends `https://` if no protocol specified
- Waits for `domcontentloaded` event
- Takes a screenshot after navigation (included in response)

```python
# Navigate to URL
{"action": "navigate", "text": "https://example.com"}

# Browser back
{"action": "navigate", "text": "back"}

# Browser forward
{"action": "navigate", "text": "forward"}
```

## DOM Reading Actions

### read_page

Get the accessibility tree (DOM structure) with element references.

| Parameter | Required | Description |
|---|---|---|
| text | No | Filter: `"interactive"` for only interactive elements, empty for all visible |

Returns a YAML-like tree with ref IDs (ref_1, ref_2, etc.) for targeting elements.

```python
# Get full page structure
{"action": "read_page"}

# Get only interactive elements (buttons, links, inputs)
{"action": "read_page", "text": "interactive"}
```

### get_page_text

Extract all text content from the page. Prioritizes article/main content.

No parameters required.

Returns structured output: title, URL, source element, and cleaned text content.

```python
{"action": "get_page_text"}
```

### find

Find elements matching a search query. Uses AI-powered semantic search when ANTHROPIC_API_KEY is available, otherwise falls back to simple text matching.

| Parameter | Required | Description |
|---|---|---|
| text | Yes | Text or description to search for |

Returns up to 20 matching elements with refs, roles, names, and descriptions.

```python
{"action": "find", "text": "login button"}
{"action": "find", "text": "email input field"}
```

## Mouse Actions

All mouse actions accept either `ref` (preferred) or `coordinate`. When using coordinates, they are automatically scaled from Claude Vision resolution to viewport resolution.

### left_click / right_click / middle_click

Click at a position or on an element.

| Parameter | Required | Description |
|---|---|---|
| coordinate | One of coordinate/ref required | [x, y] position to click |
| ref | One of coordinate/ref required | Element reference (ref_1, etc.) |
| text | No | Modifier keys to hold (e.g., "shift", "ctrl") |

```python
{"action": "left_click", "ref": "ref_5"}
{"action": "left_click", "coordinate": [728, 410]}
{"action": "right_click", "ref": "ref_12"}
```

### double_click / triple_click

Double or triple click at a position. Same parameters as click actions.

```python
{"action": "double_click", "ref": "ref_7"}   # Select word
{"action": "triple_click", "ref": "ref_7"}   # Select line/paragraph
```

### hover

Move cursor without clicking. Useful for tooltips, dropdowns, hover states.

| Parameter | Required | Description |
|---|---|---|
| coordinate | One of coordinate/ref required | [x, y] position |
| ref | One of coordinate/ref required | Element reference |

Returns a screenshot showing the hover result.

```python
{"action": "hover", "ref": "ref_3"}
```

### left_click_drag

Click and drag from one position to another.

| Parameter | Required | Description |
|---|---|---|
| start_coordinate | Yes | [x, y] starting position |
| coordinate | Yes | [x, y] ending position |

```python
{"action": "left_click_drag", "start_coordinate": [100, 200], "coordinate": [300, 400]}
```

### left_mouse_down / left_mouse_up

Fine-grained mouse button control.

| Parameter | Required | Description |
|---|---|---|
| coordinate | Yes | [x, y] position |

```python
{"action": "left_mouse_down", "coordinate": [100, 200]}
{"action": "left_mouse_up", "coordinate": [300, 400]}
```

## Keyboard Actions

### type

Type text at the current cursor position.

| Parameter | Required | Description |
|---|---|---|
| text | Yes | Text to type |

```python
{"action": "type", "text": "Hello, world!"}
```

### key

Press a key or key combination. Supports modifiers.

| Parameter | Required | Description |
|---|---|---|
| text | Yes | Key name or combination (e.g., "Enter", "ctrl+a", "cmd+c") |

Supported modifier names: `ctrl`/`control`, `cmd`/`command`/`meta`, `alt`/`option`, `shift`

```python
{"action": "key", "text": "Enter"}
{"action": "key", "text": "ctrl+a"}
{"action": "key", "text": "cmd+c"}
{"action": "key", "text": "Tab"}
{"action": "key", "text": "Escape"}
```

### hold_key

Hold down a key for a specified duration.

| Parameter | Required | Description |
|---|---|---|
| text | Yes | Key to hold |
| duration | No | Seconds to hold (default: 1.0) |

```python
{"action": "hold_key", "text": "shift", "duration": 2.0}
```

## Form Actions

### form_input

Set the value of a form input element directly. More reliable than click+type for form fields.

| Parameter | Required | Description |
|---|---|---|
| ref | Yes | Element reference |
| value | Yes | Value to set (string, number, or boolean) |

Handles different input types:
- **Text/textarea**: Sets value directly, dispatches change/input events
- **Select**: Finds option by value or text
- **Checkbox**: Requires boolean value
- **Radio**: Sets to checked
- **Date/time/range/number**: Type-appropriate handling

```python
{"action": "form_input", "ref": "ref_7", "value": "john@example.com"}
{"action": "form_input", "ref": "ref_9", "value": "Option A"}   # Select
{"action": "form_input", "ref": "ref_11", "value": true}          # Checkbox
```

## Scroll Actions

### scroll

Scroll the page in a direction.

| Parameter | Required | Description |
|---|---|---|
| scroll_direction | Yes | "up", "down", "left", "right" |
| scroll_amount | Yes | Number of scroll units |
| coordinate | No | [x, y] position to scroll at |

Returns a screenshot after scrolling.

```python
{"action": "scroll", "scroll_direction": "down", "scroll_amount": 3}
```

### scroll_to

Scroll to bring a specific element into view.

| Parameter | Required | Description |
|---|---|---|
| ref | Yes | Element reference to scroll to |

Returns a screenshot after scrolling.

```python
{"action": "scroll_to", "ref": "ref_25"}
```

## Screenshot Actions

### screenshot

Take a screenshot of the current viewport.

No parameters required.

```python
{"action": "screenshot"}
```

### zoom

Take a zoomed screenshot of a specific region.

| Parameter | Required | Description |
|---|---|---|
| region | Yes | [x1, y1, x2, y2] defining the rectangle |

```python
{"action": "zoom", "region": [100, 200, 500, 400]}
```

## JavaScript Execution

### execute_js

Execute JavaScript code in the page context.

| Parameter | Required | Description |
|---|---|---|
| text | Yes | Valid JavaScript code (code only, no explanatory text) |

Returns the result of the last expression.

```python
{"action": "execute_js", "text": "document.title"}
{"action": "execute_js", "text": "localStorage.getItem('token')"}
{"action": "execute_js", "text": "document.querySelectorAll('a').length"}
```

## Timing

### wait

Wait for a specified duration. Useful for slow-loading pages.

| Parameter | Required | Description |
|---|---|---|
| duration | No | Seconds to wait (default: 1.0, max: 100) |

```python
{"action": "wait", "duration": 2.0}
```

## Action Categories Summary

| Category | Actions | Primary Targeting |
|---|---|---|
| Navigation | navigate | URL string |
| DOM Reading | read_page, get_page_text, find | - |
| Mouse | left_click, right_click, middle_click, double_click, triple_click, hover, left_click_drag, left_mouse_down, left_mouse_up | ref or coordinate |
| Keyboard | type, key, hold_key | Current focus |
| Forms | form_input | ref (required) |
| Scrolling | scroll, scroll_to | direction or ref |
| Visual | screenshot, zoom | - or region |
| JavaScript | execute_js | Code string |
| Timing | wait | Duration |
