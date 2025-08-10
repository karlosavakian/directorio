document.addEventListener("DOMContentLoaded", () => {
  document.querySelectorAll(".form-field").forEach((field) => {
    const input = field.querySelector("input:not(.prefijo-input), textarea");
    if (!input) return;

    let btn = field.querySelector(".clear-btn");
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
      input.value = "";
      input.dispatchEvent(new Event("input", { bubbles: true }));
      toggle();
      input.focus();
    });

    input.addEventListener("focus", toggle);
    input.addEventListener("blur", toggle);
    input.addEventListener("input", toggle);
    toggle();
  });
});
