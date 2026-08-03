/**
 * DOM Extraction: Generates an accessibility tree with ref IDs.
 *
 * Inject into page via Playwright's page.evaluate(). Defines
 * window.__generateAccessibilityTree(filterType) and maintains
 * window.__claudeElementMap for persistent element references.
 *
 * Usage with Playwright:
 *   const script = fs.readFileSync('dom-extraction.js', 'utf8');
 *   const result = await page.evaluate(`
 *     (function() { ${script} return window.__generateAccessibilityTree(''); })()
 *   `);
 *   console.log(result.pageContent); // YAML-like tree
 *
 * Filter types:
 *   '' (empty)     - All visible elements (interactive, semantic, with text)
 *   'interactive'  - Only interactive elements (buttons, links, inputs, etc.)
 *   'all'          - All visible elements including off-viewport (for search)
 */

(function () {
  if (!window.__claudeElementMap) {
    window.__claudeElementMap = {};
  }
  if (!window.__claudeRefCounter) {
    window.__claudeRefCounter = 0;
  }

  window.__generateAccessibilityTree = function (filterType) {
    var result = [];

    function getRole(element) {
      var role = element.getAttribute("role");
      if (role) return role;

      var tag = element.tagName.toLowerCase();
      var type = element.getAttribute("type");

      var roleMap = {
        a: "link", button: "button",
        input: type === "submit" || type === "button" ? "button"
             : type === "checkbox" ? "checkbox"
             : type === "radio" ? "radio"
             : type === "file" ? "button" : "textbox",
        select: "combobox", textarea: "textbox",
        h1: "heading", h2: "heading", h3: "heading",
        h4: "heading", h5: "heading", h6: "heading",
        img: "image", nav: "navigation", main: "main",
        header: "banner", footer: "contentinfo",
        section: "region", article: "article",
        aside: "complementary", form: "form",
        table: "table", ul: "list", ol: "list",
        li: "listitem", label: "label",
      };
      return roleMap[tag] || "generic";
    }

    function getCleanName(element) {
      var tag = element.tagName.toLowerCase();

      // Select elements: show selected option
      if (tag === "select") {
        var sel = element;
        var opt = sel.querySelector("option[selected]") || sel.options[sel.selectedIndex];
        if (opt && opt.textContent) return opt.textContent.trim();
      }

      // Priority: aria-label > placeholder > title > alt > label > value > text
      var ariaLabel = element.getAttribute("aria-label");
      if (ariaLabel && ariaLabel.trim()) return ariaLabel.trim();

      var placeholder = element.getAttribute("placeholder");
      if (placeholder && placeholder.trim()) return placeholder.trim();

      var title = element.getAttribute("title");
      if (title && title.trim()) return title.trim();

      var alt = element.getAttribute("alt");
      if (alt && alt.trim()) return alt.trim();

      if (element.id) {
        var label = document.querySelector('label[for="' + element.id + '"]');
        if (label && label.textContent) return label.textContent.trim();
      }

      if (tag === "input") {
        var inputType = element.getAttribute("type") || "";
        var value = element.getAttribute("value");
        if (inputType === "submit" && value) return value.trim();
        if (element.value && element.value.length < 50) return element.value.trim();
      }

      if (["button", "a", "summary"].includes(tag)) {
        var text = "";
        for (var i = 0; i < element.childNodes.length; i++) {
          if (element.childNodes[i].nodeType === Node.TEXT_NODE) {
            text += element.childNodes[i].textContent;
          }
        }
        if (text.trim()) return text.trim();
      }

      if (tag.match(/^h[1-6]$/)) {
        var headingText = element.textContent;
        if (headingText) return headingText.trim().substring(0, 100);
      }

      // Direct text content for other elements
      var directText = "";
      for (var j = 0; j < element.childNodes.length; j++) {
        if (element.childNodes[j].nodeType === Node.TEXT_NODE) {
          directText += element.childNodes[j].textContent;
        }
      }
      if (directText.trim().length >= 3) {
        return directText.trim().substring(0, 50);
      }

      return "";
    }

    function isVisible(element) {
      var style = window.getComputedStyle(element);
      return (
        style.display !== "none" &&
        style.visibility !== "hidden" &&
        style.opacity !== "0" &&
        element.offsetWidth > 0 &&
        element.offsetHeight > 0
      );
    }

    function isInteractive(element) {
      var tag = element.tagName.toLowerCase();
      return (
        ["a", "button", "input", "select", "textarea", "details", "summary"].includes(tag) ||
        element.getAttribute("onclick") !== null ||
        element.getAttribute("tabindex") !== null ||
        element.getAttribute("role") === "button" ||
        element.getAttribute("role") === "link" ||
        element.getAttribute("contenteditable") === "true"
      );
    }

    function shouldInclude(element, filter) {
      var tag = element.tagName.toLowerCase();
      if (["script", "style", "meta", "link", "title", "noscript"].includes(tag)) return false;
      if (element.getAttribute("aria-hidden") === "true") return false;
      if (!isVisible(element)) return false;

      // Viewport check (skip for "all" filter used by find)
      if (filter !== "all") {
        var rect = element.getBoundingClientRect();
        if (rect.top >= window.innerHeight || rect.bottom <= 0 ||
            rect.left >= window.innerWidth || rect.right <= 0) return false;
      }

      if (filter === "interactive") return isInteractive(element);

      // Default: include interactive, semantic, or elements with text
      if (isInteractive(element)) return true;
      var role = element.getAttribute("role");
      if (role || tag.match(/^(h[1-6]|nav|main|header|footer|section|article|aside)$/)) return true;
      if (getCleanName(element).length > 0) return true;
      return false;
    }

    function processElement(element, depth, filter) {
      if (depth > 15 || !element || !element.tagName) return;

      var include = shouldInclude(element, filter) || depth === 0;

      if (include) {
        var role = getRole(element);
        var name = getCleanName(element);

        // Reuse existing ref or create new one
        var ref = null;
        for (var existingRef in window.__claudeElementMap) {
          if (window.__claudeElementMap[existingRef].deref() === element) {
            ref = existingRef;
            break;
          }
        }
        if (!ref) {
          ref = "ref_" + ++window.__claudeRefCounter;
          window.__claudeElementMap[ref] = new WeakRef(element);
        }

        var indent = "  ".repeat(depth);
        var line = indent + "- " + role;
        if (name) {
          line += ' "' + name.replace(/\s+/g, " ").substring(0, 100).replace(/"/g, '\\"') + '"';
        }
        line += " [ref=" + ref + "]";
        if (element.id) line += ' id="' + element.id + '"';
        if (element.getAttribute("href")) line += ' href="' + element.getAttribute("href") + '"';
        if (element.getAttribute("type")) line += ' type="' + element.getAttribute("type") + '"';

        result.push(line);
      }

      if (element.children && depth < 15) {
        for (var i = 0; i < element.children.length; i++) {
          processElement(element.children[i], include ? depth + 1 : depth, filter);
        }
      }
    }

    if (document.body) {
      processElement(document.body, 0, filterType);
    }

    // Clean up stale WeakRefs
    for (var ref in window.__claudeElementMap) {
      if (!window.__claudeElementMap[ref].deref()) {
        delete window.__claudeElementMap[ref];
      }
    }

    // Filter empty generic nodes
    var filtered = result.filter(function (line) {
      return !/^\s*- generic \[ref=ref_\d+\]$/.test(line);
    });

    return {
      pageContent: filtered.join("\n"),
      viewport: { width: window.innerWidth, height: window.innerHeight },
    };
  };
})();
