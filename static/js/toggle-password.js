document.addEventListener('DOMContentLoaded', () => {
  document.querySelectorAll('.form-field').forEach(field => {
    const input = field.querySelector('input[type="password"]');
    const toggle = field.querySelector('.toggle-password');
    if (!input || !toggle) return;

    toggle.setAttribute('tabindex', '-1');
    toggle.addEventListener('click', () => {
      const isPassword = input.getAttribute('type') === 'password';
      input.setAttribute('type', isPassword ? 'text' : 'password');
      toggle.classList.toggle('active', !isPassword);
    });
  });
});
