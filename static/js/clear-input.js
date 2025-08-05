document.addEventListener("DOMContentLoaded", () => {
  document.querySelectorAll(".form-field").forEach((field) => {
    const input = field.querySelector("input, textarea, select");
    const btn = field.querySelector(".clear-btn");
    if (!input || !btn) return;

    // Make clear button not tabbable
    btn.setAttribute("tabindex", "-1");

    const toggle = () => {
      if (input.value) {
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

    const eventName = input.tagName === "SELECT" ? "change" : "input";
    input.addEventListener(eventName, toggle);
    toggle();
  });
});
