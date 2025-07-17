
document.addEventListener('DOMContentLoaded', () => {
  document.querySelectorAll('.form-field select').forEach((select) => {
    const update = () => {
      select.classList.toggle('has-value', select.value !== '');
    };

    ['change', 'blur'].forEach((evt) => {
      select.addEventListener(evt, update);
    });

    update();
  });
});

