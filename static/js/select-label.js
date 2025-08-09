function initSelectLabels(root = document) {
  root.querySelectorAll('.form-field select').forEach(select => {
    if (select.dataset.initSelectLabels) return;

    let placeholder = select.querySelector('option[value=""]');
    if (!placeholder) {
      placeholder = document.createElement('option');
      placeholder.value = '';
      placeholder.textContent = '------';
      select.insertBefore(placeholder, select.firstChild);
      select.selectedIndex = 0;
    } else if (!placeholder.textContent.trim()) {
      placeholder.textContent = '------';
    }
    placeholder.hidden = true;

    const update = () => {
      select.classList.toggle('has-value', select.value !== '');
    };

    select.addEventListener('change', update);
    select.addEventListener('blur', update);

    update();
    select.dataset.initSelectLabels = 'true';
  });
}

document.addEventListener('DOMContentLoaded', () => {
  initSelectLabels();
});

window.initSelectLabels = initSelectLabels;
