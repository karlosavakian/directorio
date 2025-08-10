(function () {
  function initClearInputs(root = document) {
    let fields = [];
    if (root.classList && root.classList.contains('form-field')) {
      fields.push(root);
    }
    if (root.querySelectorAll) {
      fields = fields.concat(Array.from(root.querySelectorAll('.form-field')));
    }
    fields.forEach((field) => {
      if (field.dataset.clearInputInitialized === 'true') return;
      const input = field.querySelector('input:not(.prefijo-input), textarea');
      if (!input) return;

      let btn = field.querySelector('.clear-btn');
      if (!btn) {
        btn = document.createElement('button');
        btn.type = 'button';
        btn.className = 'clear-btn bi bi-x';
        const label = field.querySelector('label');
        if (label) {
          field.insertBefore(btn, label);
        } else {
          field.appendChild(btn);
        }
      }

      btn.setAttribute('tabindex', '-1');
      btn.addEventListener('mousedown', (e) => e.preventDefault());

      const toggle = () => {
        btn.style.display =
          document.activeElement === input && input.value ? 'block' : 'none';
      };

      btn.addEventListener('click', () => {
        input.value = '';
        input.dispatchEvent(new Event('input', { bubbles: true }));
        toggle();
        input.focus();
      });

      input.addEventListener('focus', toggle);
      input.addEventListener('blur', toggle);
      input.addEventListener('input', toggle);
      toggle();

      field.dataset.clearInputInitialized = 'true';
    });
  }

  document.addEventListener('DOMContentLoaded', () => {
    initClearInputs();
    const observer = new MutationObserver((mutations) => {
      mutations.forEach((m) => {
        m.addedNodes.forEach((node) => {
          if (node.nodeType === 1) {
            initClearInputs(node);
          }
        });
      });
    });
    observer.observe(document.body, { childList: true, subtree: true });
  });

  window.initClearInputs = initClearInputs;
})();
