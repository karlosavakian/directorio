document.addEventListener("DOMContentLoaded", () => {
  document.querySelectorAll(".form-field").forEach((field) => {
    const input = field.querySelector("input:not(.prefijo-input), textarea, select");
    if (!input) return;

    // Skip textareas completely
    if (input.tagName === "TEXTAREA") return;

    let btn = field.querySelector(".clear-btn");

    // Create clear button if not present
    if (!btn) {
      btn = document.createElement("button");
      btn.type = "button";
      btn.className = "clear-btn bi bi-x";
      const label = field.querySelector("label");
      if (label) {
        field.insertBefore(btn, label);
      } else {
        field.appendChild(btn);
      }
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
