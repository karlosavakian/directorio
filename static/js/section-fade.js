document.addEventListener('DOMContentLoaded', () => {
  document.querySelectorAll('.fade-section').forEach(el => {
    requestAnimationFrame(() => el.classList.add('show'));
  });
});
