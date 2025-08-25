document.addEventListener('DOMContentLoaded', () => {
  const aboutInput = document.getElementById('id_about');
  if (!aboutInput) return;
  const original = aboutInput.getAttribute('placeholder');
  aboutInput.addEventListener('focus', () => {
    aboutInput.setAttribute('data-placeholder', original);
    aboutInput.setAttribute('placeholder', '');
  });
  aboutInput.addEventListener('blur', () => {
    if (!aboutInput.value.trim()) {
      const restore = aboutInput.getAttribute('data-placeholder') || '';
      aboutInput.setAttribute('placeholder', restore);
    }
  });
});
