document.addEventListener('DOMContentLoaded', () => {
  document.querySelectorAll('.feature-option').forEach(option => {
    const checkbox = option.querySelector('input[type="checkbox"]');
    if (checkbox.checked) {
      option.classList.add('selected');
    }
    option.addEventListener('click', () => {
      checkbox.checked = !checkbox.checked;
      option.classList.toggle('selected', checkbox.checked);
    });
  });
});
