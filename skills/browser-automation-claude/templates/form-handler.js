/**
 * Form Handler: Manipulates form input elements by ref ID.
 *
 * Requires window.__claudeElementMap to be populated by dom-extraction.js.
 *
 * Supports:
 *   - Text inputs and textareas (string value)
 *   - Select dropdowns (match by value or visible text)
 *   - Checkboxes (boolean value)
 *   - Radio buttons (sets to checked)
 *   - Date, time, datetime-local, month, week (string value)
 *   - Range and number inputs (numeric value)
 *
 * Usage with Playwright:
 *   const script = fs.readFileSync('form-handler.js', 'utf8');
 *   const result = await page.evaluate(`(${script})("ref_7", "hello@example.com")`);
 *   if (result.success) console.log(result.message);
 *
 * Returns:
 *   {
 *     success: boolean,
 *     action: 'form_input',
 *     ref: string,
 *     element_type: string,
 *     previous_value: any,
 *     new_value: any,
 *     message: string,
 *   }
 */

(function (elementRef, inputValue) {
  try {
    // Look up element from ref map
    var element = null;

    if (window.__claudeElementMap && window.__claudeElementMap[elementRef]) {
      var weakRef = window.__claudeElementMap[elementRef];
      element = weakRef.deref() || null;

      if (!element || !document.contains(element)) {
        delete window.__claudeElementMap[elementRef];
        element = null;
      }
    }

    if (!element) {
      return {
        success: false,
        action: "form_input",
        message:
          'No element found with reference: "' +
          elementRef +
          '". The element may have been removed.',
      };
    }

    // Scroll into view
    element.scrollIntoView({ behavior: "smooth", block: "center" });

    // Dispatch change and input events after setting value
    function dispatchEvents(el) {
      el.focus();
      el.dispatchEvent(new Event("change", { bubbles: true }));
      el.dispatchEvent(new Event("input", { bubbles: true }));
    }

    // --- Select elements ---
    if (element instanceof HTMLSelectElement) {
      var previousValue = element.value;
      var options = Array.from(element.options);
      var valueStr = String(inputValue);
      var found = false;

      for (var i = 0; i < options.length; i++) {
        if (options[i].value === valueStr || options[i].text === valueStr) {
          element.selectedIndex = i;
          found = true;
          break;
        }
      }

      if (!found) {
        return {
          success: false,
          action: "form_input",
          message:
            'Option "' +
            valueStr +
            '" not found. Available: ' +
            options
              .map(function (o) {
                return '"' + o.text + '" (value: "' + o.value + '")';
              })
              .join(", "),
        };
      }

      dispatchEvents(element);
      return {
        success: true,
        action: "form_input",
        ref: elementRef,
        element_type: "select",
        previous_value: previousValue,
        new_value: element.value,
        message: 'Selected "' + valueStr + '"',
      };
    }

    // --- Checkbox ---
    if (element instanceof HTMLInputElement && element.type === "checkbox") {
      var prevChecked = element.checked;
      if (typeof inputValue !== "boolean") {
        return {
          success: false,
          action: "form_input",
          message: "Checkbox requires a boolean value (true/false)",
        };
      }
      element.checked = inputValue;
      dispatchEvents(element);
      return {
        success: true,
        action: "form_input",
        ref: elementRef,
        element_type: "checkbox",
        previous_value: prevChecked,
        new_value: element.checked,
        message: "Checkbox " + (element.checked ? "checked" : "unchecked"),
      };
    }

    // --- Radio ---
    if (element instanceof HTMLInputElement && element.type === "radio") {
      var prevRadio = element.checked;
      element.checked = true;
      dispatchEvents(element);
      return {
        success: true,
        action: "form_input",
        ref: elementRef,
        element_type: "radio",
        previous_value: prevRadio,
        new_value: true,
        message:
          "Radio selected" +
          (element.name ? ' in group "' + element.name + '"' : ""),
      };
    }

    // --- Date/time types ---
    if (
      element instanceof HTMLInputElement &&
      ["date", "time", "datetime-local", "month", "week"].includes(element.type)
    ) {
      var prevDate = element.value;
      element.value = String(inputValue);
      dispatchEvents(element);
      return {
        success: true,
        action: "form_input",
        ref: elementRef,
        element_type: element.type,
        previous_value: prevDate,
        new_value: element.value,
        message: "Set " + element.type + ' to "' + element.value + '"',
      };
    }

    // --- Range ---
    if (element instanceof HTMLInputElement && element.type === "range") {
      var prevRange = element.value;
      var numVal = Number(inputValue);
      if (isNaN(numVal)) {
        return {
          success: false,
          action: "form_input",
          message: "Range input requires a numeric value",
        };
      }
      element.value = String(numVal);
      dispatchEvents(element);
      return {
        success: true,
        action: "form_input",
        ref: elementRef,
        element_type: "range",
        previous_value: prevRange,
        new_value: element.value,
        message:
          "Set range to " +
          element.value +
          " (min: " +
          element.min +
          ", max: " +
          element.max +
          ")",
      };
    }

    // --- Number ---
    if (element instanceof HTMLInputElement && element.type === "number") {
      var prevNum = element.value;
      var nv = Number(inputValue);
      if (isNaN(nv) && inputValue !== "") {
        return {
          success: false,
          action: "form_input",
          message: "Number input requires a numeric value",
        };
      }
      element.value = String(inputValue);
      dispatchEvents(element);
      return {
        success: true,
        action: "form_input",
        ref: elementRef,
        element_type: "number",
        previous_value: prevNum,
        new_value: element.value,
        message: "Set number to " + element.value,
      };
    }

    // --- Text input / textarea ---
    if (
      element instanceof HTMLInputElement ||
      element instanceof HTMLTextAreaElement
    ) {
      var prevText = element.value;
      element.value = String(inputValue);
      element.focus();
      element.setSelectionRange(element.value.length, element.value.length);
      element.dispatchEvent(new Event("change", { bubbles: true }));
      element.dispatchEvent(new Event("input", { bubbles: true }));

      var elType =
        element instanceof HTMLTextAreaElement
          ? "textarea"
          : element.type || "text";
      return {
        success: true,
        action: "form_input",
        ref: elementRef,
        element_type: elType,
        previous_value: prevText,
        new_value: element.value,
        message: "Set " + elType + ' to "' + element.value + '"',
      };
    }

    // --- Unsupported element ---
    return {
      success: false,
      action: "form_input",
      message:
        'Element type "' +
        element.tagName +
        '" is not a supported form input',
    };
  } catch (error) {
    return {
      success: false,
      action: "form_input",
      message:
        "Error setting form value: " + (error.message || "Unknown error"),
    };
  }
})
