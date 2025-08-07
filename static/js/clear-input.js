document.addEventListener("DOMContentLoaded", () => {
  document.querySelectorAll(".form-field").forEach((field) => {
    const input = field.querySelector("input:not(.prefijo-input), textarea, select");
    const btn = field.querySelector(".clear-btn");
    if (!input || !btn) return;

    // Remove clear button for textareas
    if (input.tagName === "TEXTAREA") {
      btn.remove();
      return;
    }

    // Make clear button not tabbable
    btn.setAttribute("tabindex", "-1");
    btn.addEventListener("mousedown", (e) => e.preventDefault());

    const toggle = () => {
      if (document.activeElement === input && input.value) {
        btn.style.display = "block";
      } else {
        btn.style.display = "none";
      }
    };

    btn.addEventListener("click", () => {
      if (input.tagName === "SELECT") {
        input.selectedIndex = 0;
        input.dispatchEvent(new Event("change", { bubbles: true }));
      } else {
        input.value = "";
        input.dispatchEvent(new Event("input", { bubbles: true }));
      }
      toggle();
      input.focus();
    });

    input.addEventListener("focus", toggle);
    input.addEventListener("blur", toggle);
    const eventName = input.tagName === "SELECT" ? "change" : "input";
    input.addEventListener(eventName, toggle);
    toggle();
  });
});
