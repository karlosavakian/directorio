document.addEventListener('DOMContentLoaded', () => {
  const toggleBtn = document.getElementById('member-search-toggle');
  const wrapper = document.getElementById('member-search-wrapper');
  const input = document.getElementById('member-search-input');
  if (toggleBtn) {
    toggleBtn.addEventListener('click', () => {
      if (wrapper) {
        wrapper.classList.toggle('show');
        if (wrapper.classList.contains('show')) {
          input.focus();
        } else {
          input.value = '';
        }
      }
    });
  }
  if (input) {
    const listId = input.getAttribute('list');
    input.addEventListener('input', () => {
      if (input.value.trim().length > 0) {
        input.setAttribute('list', listId);
      } else {
        input.removeAttribute('list');
      }
    });
  }
});
