document.addEventListener('DOMContentLoaded', () => {
  const options = document.querySelectorAll('.feature-option');
  const selectAllBtn = document.getElementById('features-select-all');
  const deselectAllBtn = document.getElementById('features-deselect-all');

  const updateButtons = () => {
    const anySelected = Array.from(options).some(option => {
      const checkbox = option.querySelector('input[type="checkbox"]');
      return checkbox && checkbox.checked;
    });
    if (deselectAllBtn) {
      deselectAllBtn.classList.toggle('text-secondary', !anySelected);
      deselectAllBtn.classList.toggle('text-black', anySelected);
    }
  };

  options.forEach(option => {
    const checkbox = option.querySelector('input[type="checkbox"]');
    if (checkbox.checked) {
      option.classList.add('selected');
    }
    option.addEventListener('click', () => {
      checkbox.checked = !checkbox.checked;
      option.classList.toggle('selected', checkbox.checked);
      updateButtons();
    });
  });

  selectAllBtn &&
    selectAllBtn.addEventListener('click', () => {
      options.forEach(option => {
        const checkbox = option.querySelector('input[type="checkbox"]');
        checkbox.checked = true;
        option.classList.add('selected');
      });
      updateButtons();
    });

  deselectAllBtn &&
    deselectAllBtn.addEventListener('click', () => {
      options.forEach(option => {
        const checkbox = option.querySelector('input[type="checkbox"]');
        checkbox.checked = false;
        option.classList.remove('selected');
      });
      updateButtons();
    });

  updateButtons();
});
