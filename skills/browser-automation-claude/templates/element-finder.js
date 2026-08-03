/**
 * Element Finder: Locates elements by ref ID, scrolls into view,
 * and returns coordinates and metadata.
 *
 * Requires window.__claudeElementMap to be populated by dom-extraction.js.
 *
 * Usage with Playwright:
 *   const script = fs.readFileSync('element-finder.js', 'utf8');
 *   const result = await page.evaluate(`(${script})("ref_5")`);
 *   if (result.success) {
 *     await page.mouse.click(result.coordinates[0], result.coordinates[1]);
 *   }
 *
 * Returns:
 *   {
 *     success: boolean,
 *     coordinates: [x, y],        // Center of element in viewport
 *     elementInfo: string,         // e.g. "button#submit.btn.primary"
 *     rect: { left, top, right, bottom, width, height },
 *     attributes: { type, role, ariaLabel, text },
 *     isVisible: boolean,
 *     isInteractable: boolean,
 *   }
 */

(function (elementRef) {
  try {
    var targetElement = null;

    if (window.__claudeElementMap && window.__claudeElementMap[elementRef]) {
      var weakRef = window.__claudeElementMap[elementRef];
      targetElement = weakRef.deref() || null;

      if (!targetElement || !document.contains(targetElement)) {
        delete window.__claudeElementMap[elementRef];
        targetElement = null;
      }
    }

    if (!targetElement) {
      return {
        success: false,
        action: "get_element",
        message:
          'No element found with reference: "' +
          elementRef +
          '". The element may have been removed from the page.',
      };
    }

    // Scroll element into view
    targetElement.scrollIntoView({
      behavior: "instant",
      block: "center",
      inline: "center",
    });

    // Force layout recalculation
    targetElement.offsetHeight;

    // Get element coordinates (center point)
    var rect = targetElement.getBoundingClientRect();
    var clickX = rect.left + rect.width / 2;
    var clickY = rect.top + rect.height / 2;

    // Build element info string
    var info =
      targetElement.tagName.toLowerCase() +
      (targetElement.id ? "#" + targetElement.id : "") +
      (targetElement.className
        ? "." +
          targetElement.className
            .split(" ")
            .filter(function (c) {
              return c;
            })
            .join(".")
        : "");

    return {
      success: true,
      coordinates: [clickX, clickY],
      elementInfo: info,
      elementRef: elementRef,
      rect: {
        left: rect.left,
        top: rect.top,
        right: rect.right,
        bottom: rect.bottom,
        width: rect.width,
        height: rect.height,
      },
      attributes: {
        type: targetElement.getAttribute("type") || "",
        role: targetElement.getAttribute("role") || "",
        ariaLabel: targetElement.getAttribute("aria-label") || "",
        text: targetElement.textContent
          ? targetElement.textContent.substring(0, 100)
          : "",
      },
      isVisible: rect.width > 0 && rect.height > 0,
      isInteractable:
        !targetElement.disabled &&
        targetElement.style.display !== "none" &&
        targetElement.style.visibility !== "hidden",
    };
  } catch (error) {
    return {
      success: false,
      action: "get_element",
      message:
        "Error finding element by reference: " +
        (error.message || "Unknown error"),
    };
  }
})
