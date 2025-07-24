document.addEventListener('DOMContentLoaded', () => {
  const dropdown = document.getElementById('booking-sort-dropdown');
  if (!dropdown) return;
  const selected = dropdown.querySelector('.selected-text');
  const menu = document.getElementById('booking-sort-menu');
  const input = document.getElementById('booking-sort-input');

  dropdown.querySelector('.selected').addEventListener('click', (e) => {
    e.stopPropagation();
    menu.style.display = menu.style.display === 'block' ? 'none' : 'block';
  });

  menu.querySelectorAll('.dropdown-item').forEach(item => {
    item.addEventListener('click', () => {
      selected.textContent = item.textContent;
      input.value = item.dataset.value;
      menu.style.display = 'none';
      dropdown.closest('form').submit();
    });
  });

  document.addEventListener('click', () => {
    menu.style.display = 'none';
  });
});
