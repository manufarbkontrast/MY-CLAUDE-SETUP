# Coordinate Scaling

Claude Vision processes images at different resolutions than the actual browser viewport. When Claude identifies a coordinate in a screenshot, that coordinate is relative to the processed image dimensions, not the actual viewport. Coordinate scaling maps Claude's coordinates to the correct browser viewport position.

## The Problem

- Browser viewport: 1920x1080 (typical full HD)
- Claude Vision processes 16:9 images at: 1456x819
- Claude reports coordinates in the 1456x819 space
- Playwright needs coordinates in the 1920x1080 space
- Without scaling, clicks land in the wrong position

## Scale Formulas

```
scaled_x = int(x * viewport_width / CLAUDE_ACTUAL_WIDTH)
scaled_y = int(y * viewport_height / CLAUDE_ACTUAL_HEIGHT)
```

For the standard 1920x1080 viewport with 16:9 aspect ratio:

```
scale_x = 1920 / 1456 = 1.3187...
scale_y = 1080 / 819  = 1.3187...
```

So a coordinate Claude reports as (728, 410) maps to approximately (960, 540) in the viewport -- the center of the screen.

## Claude Vision Processing Resolutions

Claude resizes images while preserving aspect ratio. The documented sizes for different aspect ratios:

| Aspect Ratio | Dimensions | Use Case |
|---|---|---|
| 1:1 | 1092x1092 | Square |
| 3:4 | 951x1268 | Portrait |
| 4:3 | 1268x951 | Landscape |
| 2:3 | 896x1344 | Portrait |
| 3:2 | 1344x896 | Landscape |
| 9:16 | 819x1456 | Portrait (phone) |
| **16:9** | **1456x819** | **Landscape (browser)** |
| 1:2 | 784x1568 | Portrait (tall) |
| 2:1 | 1568x784 | Landscape (wide) |

For browser automation, the 16:9 ratio (1456x819) is the standard. See the [Claude Vision docs](https://docs.claude.com/en/docs/build-with-claude/vision#evaluate-image-size).

## Threshold Checking

Before scaling, check whether coordinates actually need it. This prevents double-scaling if coordinates are already in viewport space:

```python
# If coordinates exceed Claude's resolution with 20% margin,
# they are likely already in viewport coordinates
max_expected_x = CLAUDE_ACTUAL_WIDTH * 1.2   # 1747
max_expected_y = CLAUDE_ACTUAL_HEIGHT * 1.2   # 983

if x > max_expected_x or y > max_expected_y:
    # Already in viewport coordinates, skip scaling
    return x, y
```

Also skip scaling when scale factors are very close to 1.0 (viewport matches Claude resolution):

```python
if abs(scale_x - 1.0) < 0.05 and abs(scale_y - 1.0) < 0.05:
    return x, y
```

## CoordinateScaler Class

The complete, reusable scaler (also available in `templates/coordinate-scaler.py`):

```python
class CoordinateScaler:
    """Handles coordinate scaling between Claude's vision and actual viewport."""

    # Claude's image processing resolution for 16:9 aspect ratio
    CLAUDE_ACTUAL_WIDTH = 1456
    CLAUDE_ACTUAL_HEIGHT = 819

    DOCUMENTED_SIZES = {
        (1, 1): (1092, 1092),
        (3, 4): (951, 1268),
        (4, 3): (1268, 951),
        (2, 3): (896, 1344),
        (3, 2): (1344, 896),
        (9, 16): (819, 1456),
        (16, 9): (1456, 819),
        (1, 2): (784, 1568),
        (2, 1): (1568, 784),
    }

    @classmethod
    def get_scale_factors(
        cls,
        viewport_width: int,
        viewport_height: int,
    ) -> tuple[float, float]:
        scale_x = viewport_width / cls.CLAUDE_ACTUAL_WIDTH
        scale_y = viewport_height / cls.CLAUDE_ACTUAL_HEIGHT
        return scale_x, scale_y

    @classmethod
    def scale_coordinates(
        cls,
        x: int,
        y: int,
        viewport_width: int,
        viewport_height: int,
        apply_threshold: bool = True,
    ) -> tuple[int, int]:
        scale_x, scale_y = cls.get_scale_factors(viewport_width, viewport_height)

        # No scaling needed if factors are close to 1.0
        if abs(scale_x - 1.0) < 0.05 and abs(scale_y - 1.0) < 0.05:
            return x, y

        if apply_threshold:
            max_expected_x = cls.CLAUDE_ACTUAL_WIDTH * 1.2
            max_expected_y = cls.CLAUDE_ACTUAL_HEIGHT * 1.2
            if x > max_expected_x or y > max_expected_y:
                return x, y

        scaled_x = int(x * scale_x)
        scaled_y = int(y * scale_y)

        # Clamp to viewport bounds
        scaled_x = min(scaled_x, viewport_width - 1)
        scaled_y = min(scaled_y, viewport_height - 1)

        return scaled_x, scaled_y
```

## Integration with BrowserTool

The BrowserTool applies scaling automatically on every coordinate-based action:

```python
class BrowserTool:
    def __init__(self):
        self.width = 1920   # BROWSER_WIDTH
        self.height = 1080  # BROWSER_HEIGHT

    def _scale_coordinates(self, x: int, y: int) -> tuple[int, int]:
        return CoordinateScaler.scale_coordinates(
            x, y, self.width, self.height
        )

    async def _click(self, action, coordinate=None, ref=None, **kwargs):
        if coordinate:
            x, y = coordinate
            x, y = self._scale_coordinates(x, y)
            await self._page.mouse.click(x, y)
        elif ref:
            # Ref-based clicks bypass coordinate scaling entirely
            element_info = await self._execute_js("element_script.js", ref)
            click_x, click_y = element_info["coordinates"]
            await self._page.mouse.click(click_x, click_y)
```

Note that ref-based interactions do NOT need coordinate scaling because the JavaScript returns coordinates already in viewport space.

## When to Use Coordinate Scaling

| Scenario | Needs Scaling? |
|---|---|
| Claude reports click coordinates from screenshot | Yes |
| Element found via ref (DOM-based) | No |
| Drag start/end coordinates from Claude | Yes |
| Mouse down/up coordinates from Claude | Yes |
| Coordinates from JavaScript element lookup | No |

## Best Practices

1. **Always prefer refs over coordinates** - They are more reliable and skip scaling entirely
2. **Use 16:9 viewport** (1920x1080) for consistent scaling with Claude Vision
3. **Log scaling** for debugging: `print(f"Scaled ({x}, {y}) -> ({scaled_x}, {scaled_y})")`
4. **Validate bounds** after scaling to prevent out-of-viewport clicks
5. **Match aspect ratios** - If using a non-standard viewport, use `get_documented_size_for_aspect_ratio()` to find the correct Claude processing resolution
