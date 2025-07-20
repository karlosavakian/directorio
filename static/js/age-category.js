function initAgeCategory(root = document) {
  const ageInput = root.querySelector('input[name="edad"]');
  const select = root.querySelector('select[name="modalidad"]');
  if (!ageInput || !select) return;

  const update = () => {
    const age = parseInt(ageInput.value, 10);
    let value = '';
    if (!isNaN(age)) {
      if (age >= 13 && age <= 14) {
        value = 'schoolboy';
      } else if (age >= 15 && age <= 16) {
        value = 'junior';
      } else if (age >= 17 && age <= 18) {
        value = 'joven';
      } else if (age >= 19 && age <= 40) {
        value = 'elite';
      } else if (age >= 18) {
        value = 'profesional';
      }
    }
    select.value = value;
    select.dispatchEvent(new Event('change'));
  };

  ageInput.addEventListener('input', update);
  update();
}

document.addEventListener('DOMContentLoaded', () => {
  initAgeCategory();
});

window.initAgeCategory = initAgeCategory;
