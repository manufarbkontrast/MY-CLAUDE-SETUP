"""
Standalone CoordinateScaler for mapping Claude Vision coordinates to viewport coordinates.

Claude's vision model processes images at specific resolutions based on aspect ratio.
For 16:9 (standard browser), images are processed at 1456x819.
This scaler maps coordinates from Claude's space to the actual viewport.

Usage:
    scaler = CoordinateScaler()
    scaled_x, scaled_y = scaler.scale_coordinates(728, 410, 1920, 1080)
    # Result: approximately (960, 540) -- center of 1920x1080 viewport
"""


class CoordinateScaler:
    """Handles coordinate scaling between Claude Vision and actual viewport."""

    # Claude's image processing resolution for 16:9 aspect ratio
    # Source: https://docs.claude.com/en/docs/build-with-claude/vision#evaluate-image-size
    CLAUDE_ACTUAL_WIDTH = 1456
    CLAUDE_ACTUAL_HEIGHT = 819

    # Documented maximum image sizes for different aspect ratios
    DOCUMENTED_SIZES: dict[tuple[int, int], tuple[int, int]] = {
        (1, 1): (1092, 1092),      # Square
        (3, 4): (951, 1268),       # Portrait
        (4, 3): (1268, 951),       # Landscape
        (2, 3): (896, 1344),       # Portrait
        (3, 2): (1344, 896),       # Landscape
        (9, 16): (819, 1456),      # Portrait (phone)
        (16, 9): (1456, 819),      # Landscape (widescreen)
        (1, 2): (784, 1568),       # Portrait (tall)
        (2, 1): (1568, 784),       # Landscape (wide)
    }

    @classmethod
    def get_documented_size_for_aspect_ratio(
        cls, viewport_width: int, viewport_height: int
    ) -> tuple[int, int]:
        """
        Get the documented Claude processing size for the viewport's aspect ratio.

        Args:
            viewport_width: Actual viewport width
            viewport_height: Actual viewport height

        Returns:
            Tuple of (width, height) from documented sizes

        Raises:
            ValueError: If the aspect ratio doesn't match any documented sizes
        """
        viewport_ratio = viewport_width / viewport_height
        tolerance = 0.02

        for (ratio_w, ratio_h), (doc_w, doc_h) in cls.DOCUMENTED_SIZES.items():
            if abs(viewport_ratio - ratio_w / ratio_h) < tolerance:
                return (doc_w, doc_h)

        supported = [f"{w}:{h}" for (w, h) in cls.DOCUMENTED_SIZES]
        raise ValueError(
            f"Viewport ratio {viewport_ratio:.3f} ({viewport_width}x{viewport_height}) "
            f"not supported. Use one of: {', '.join(supported)}"
        )

    @classmethod
    def get_scale_factors(
        cls,
        viewport_width: int,
        viewport_height: int,
        match_aspect_ratio: bool = False,
    ) -> tuple[float, float]:
        """
        Calculate scale factors for Claude coordinates -> viewport coordinates.

        Args:
            viewport_width: Actual browser viewport width
            viewport_height: Actual browser viewport height
            match_aspect_ratio: If True, auto-detect aspect ratio.
                If False, assume 16:9 (standard browser).

        Returns:
            Tuple of (scale_x, scale_y)
        """
        if match_aspect_ratio:
            base_w, base_h = cls.get_documented_size_for_aspect_ratio(
                viewport_width, viewport_height
            )
        else:
            base_w = cls.CLAUDE_ACTUAL_WIDTH
            base_h = cls.CLAUDE_ACTUAL_HEIGHT

        return viewport_width / base_w, viewport_height / base_h

    @classmethod
    def scale_coordinates(
        cls,
        x: int,
        y: int,
        viewport_width: int,
        viewport_height: int,
        apply_threshold: bool = True,
    ) -> tuple[int, int]:
        """
        Scale coordinates from Claude's vision space to viewport space.

        Args:
            x: X coordinate from Claude
            y: Y coordinate from Claude
            viewport_width: Actual browser viewport width
            viewport_height: Actual browser viewport height
            apply_threshold: Check if coordinates need scaling (prevents double-scaling)

        Returns:
            Tuple of (scaled_x, scaled_y)
        """
        scale_x, scale_y = cls.get_scale_factors(viewport_width, viewport_height)

        # No scaling needed if factors are close to 1.0
        if abs(scale_x - 1.0) < 0.05 and abs(scale_y - 1.0) < 0.05:
            return x, y

        if apply_threshold:
            # If coordinates already exceed Claude's resolution,
            # they are likely already in viewport space
            max_x = cls.CLAUDE_ACTUAL_WIDTH * 1.2
            max_y = cls.CLAUDE_ACTUAL_HEIGHT * 1.2
            if x > max_x or y > max_y:
                return x, y

        scaled_x = min(int(x * scale_x), viewport_width - 1)
        scaled_y = min(int(y * scale_y), viewport_height - 1)

        return scaled_x, scaled_y

    @classmethod
    def scale_coordinate_pair(
        cls,
        coords: list | tuple,
        viewport_width: int,
        viewport_height: int,
    ) -> list[int]:
        """
        Scale a [x, y] coordinate pair.

        Args:
            coords: [x, y] coordinate pair
            viewport_width: Actual browser viewport width
            viewport_height: Actual browser viewport height

        Returns:
            Scaled [x, y] coordinate pair
        """
        if not isinstance(coords, (list, tuple)) or len(coords) != 2:
            return list(coords) if isinstance(coords, tuple) else coords

        scaled_x, scaled_y = cls.scale_coordinates(
            coords[0], coords[1], viewport_width, viewport_height
        )
        return [scaled_x, scaled_y]
