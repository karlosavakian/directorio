document.addEventListener("DOMContentLoaded", () => {
  document.querySelectorAll(".form-field").forEach((field) => {
    const input = field.querySelector("input");
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
      input.value = "";
      input.dispatchEvent(new Event("input", { bubbles: true }));
      toggle();
      input.focus();
    });

    input.addEventListener("input", toggle);
    toggle();
  });
});
