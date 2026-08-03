# DOM Interaction Patterns

DOM-based interaction is the preferred method for browser automation with Claude. Instead of relying on pixel coordinates from screenshots (which are fragile and resolution-dependent), the system injects JavaScript to generate an accessibility tree with stable element references.

## Why DOM-Based Beats Pixel Coordinates

| Feature | DOM-Based (refs) | Coordinate-Based |
|---|---|---|
| Resolution independent | Yes | No - breaks on resize |
| Reliable targeting | Yes - refs point to elements | No - coordinates drift |
| Works with dynamic content | Yes - refs update on read_page | No - layout changes break it |
| Coordinate scaling needed | No | Yes - must map Claude vision to viewport |
| Works with hidden elements | Yes - can scroll into view | No - must be visible |
| Form manipulation | Yes - direct value setting | No - must click and type |

The recommended workflow is:
1. Navigate to a page
2. Call `read_page` to get the accessibility tree with refs
3. Use refs for all subsequent interactions (click, type, form_input, etc.)
4. Fall back to coordinates only when refs fail

## Global Element Map

The system maintains a global element map on the page using WeakRefs:

```javascript
// Initialized on first read_page call
window.__claudeElementMap = {};    // ref_id -> WeakRef(element)
window.__claudeRefCounter = 0;     // Monotonically increasing counter
```

Key design decisions:
- **WeakRef**: Elements can be garbage collected if removed from DOM. Stale refs are cleaned up on each tree generation.
- **Global scope**: The map persists across multiple `read_page` calls. Existing refs are reused if the element still exists.
- **Monotonic counter**: Refs are never reused. `ref_1` always refers to the same element (or nothing if GC'd).

## Accessibility Tree Generation

The `read_page` action injects JavaScript that walks the DOM and generates a YAML-like tree:

```
- generic [ref=ref_1]
  - navigation "Main Menu" [ref=ref_2]
    - link "Home" [ref=ref_3] href="/"
    - link "About" [ref=ref_4] href="/about"
  - main [ref=ref_5]
    - heading "Welcome" [ref=ref_6]
    - textbox "Search" [ref=ref_7] placeholder="Search..."
    - button "Submit" [ref=ref_8]
  - complementary [ref=ref_9]
    - link "Sign Up" [ref=ref_10] href="/signup"
```

Each line contains:
- **Role**: Semantic role (link, button, textbox, heading, etc.)
- **Name**: Human-readable label (from aria-label, placeholder, text content, etc.)
- **Ref**: Unique reference ID for targeting
- **Attributes**: Useful properties (href, type, placeholder, id)

### Role Mapping

HTML elements map to semantic roles:

```javascript
var roleMap = {
    a: "link",
    button: "button",
    input: /* depends on type: "button", "checkbox", "radio", "textbox" */,
    select: "combobox",
    textarea: "textbox",
    h1: "heading", h2: "heading", /* ... h6 */
    img: "image",
    nav: "navigation",
    main: "main",
    header: "banner",
    footer: "contentinfo",
    section: "region",
    article: "article",
    aside: "complementary",
    form: "form",
    table: "table",
    ul: "list", ol: "list",
    li: "listitem",
    label: "label",
};
// Elements with explicit role="" attribute use that role
// Everything else: "generic"
```

### Name Resolution Priority

The accessible name is resolved in this order:
1. `aria-label` attribute
2. `placeholder` attribute
3. `title` attribute
4. `alt` attribute (images)
5. Associated `<label>` element (via `for` attribute)
6. Input `value` (for submit buttons and short values)
7. Direct text content (for buttons, links, headings)
8. Image filename (for images without alt)
9. Direct text nodes (for generic elements, 3+ chars)

### Element Filtering

Not all DOM elements appear in the tree. The filter logic:

**Always excluded**: script, style, meta, link, title, noscript, aria-hidden="true"

**Visibility check**: Elements must have `display !== "none"`, `visibility !== "hidden"`, `opacity !== "0"`, and non-zero dimensions.

**Viewport check**: By default, only elements visible in the current viewport are included (unless using the "all" filter for the find tool).

**Filter modes**:
- No filter (default): Interactive elements, semantic elements, and elements with meaningful text
- `"interactive"`: Only interactive elements (inputs, buttons, links, etc.)
- `"all"`: All visible elements regardless of viewport (used by the find tool)

## JavaScript Injection Pattern

JavaScript files are loaded from disk and evaluated in the page context:

```python
async def _execute_js_from_file(self, filename: str, *args):
    script_path = BROWSER_TOOL_UTILS_DIR / filename
    script = script_path.read_text()

    if filename == "browser_dom_script.js":
        # DOM script defines a function on window, then call it
        combined = f"""
            (function() {{
                {script}
                return window.__generateAccessibilityTree('{args[0]}');
            }})()
        """
        return await self._page.evaluate(combined)
    else:
        # Other scripts are IIFEs that take arguments
        escaped_args = ", ".join(json.dumps(arg) for arg in args)
        return await self._page.evaluate(f"({script})({escaped_args})")
```

Two injection patterns:
1. **Window function** (DOM script): Defines `window.__generateAccessibilityTree`, then calls it. This persists the element map across calls.
2. **IIFE with arguments** (element/form/text scripts): Wrapped as immediately-invoked function expressions receiving serialized arguments.

## Ref-Based Element Interaction

Once you have refs from `read_page`, use them for interactions:

```python
# Click an element by ref
await browser_tool(action="left_click", ref="ref_8")

# Fill a form field by ref
await browser_tool(action="form_input", ref="ref_7", value="search query")

# Scroll to an element
await browser_tool(action="scroll_to", ref="ref_10")

# Hover over an element
await browser_tool(action="hover", ref="ref_4")
```

The element script (`browser_element_script.js`) handles ref resolution:
1. Look up the WeakRef in `window.__claudeElementMap`
2. Dereference it (returns null if GC'd or removed)
3. Verify element is still in the document
4. Scroll element into view with `scrollIntoView({ block: 'center' })`
5. Get bounding rect and return center coordinates
6. Return element metadata (tag, id, class, role, aria-label, text)

## Stale Reference Handling

References can become stale when:
- The page navigates to a new URL
- DOM elements are dynamically removed
- JavaScript frameworks re-render components

The system handles this gracefully:
- WeakRefs allow garbage collection of removed elements
- On each `read_page` call, stale entries are cleaned up
- Element script returns a clear error when a ref is invalid
- Claude can call `read_page` again to get fresh refs

```javascript
// Cleanup in DOM script
for (var ref in window.__claudeElementMap) {
    var weakRef = window.__claudeElementMap[ref];
    if (!weakRef.deref()) {
        delete window.__claudeElementMap[ref];
    }
}
```

## Best Practices

1. **Always call `read_page` after navigation** to populate the element map
2. **Use `read_page` with "interactive" filter** when you only need clickable elements (faster, less noise)
3. **Re-call `read_page` after major DOM changes** (form submissions, AJAX updates, SPA navigation)
4. **Prefer refs for all interactions** - only fall back to coordinates when refs fail
5. **Use `form_input` instead of click+type** for form fields - it is more reliable and handles select elements, checkboxes, radios, etc.
