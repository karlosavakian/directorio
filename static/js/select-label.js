
document.addEventListener('DOMContentLoaded', () => {
  document.querySelectorAll('.form-field select').forEach((select) => {
    const update = () => {
      select.classList.toggle('has-value', select.value !== '');
    };

    ['change', 'blur'].forEach((evt) => {
      select.addEventListener(evt, update);
    });

  document.querySelectorAll('.form-field select').forEach(select => {
    const update = () => {
      if (select.value) {
        select.classList.add('has-value');
      } else {
        select.classList.remove('has-value');
      }
    };
    select.addEventListener('change', update);
    update();
  });
});

