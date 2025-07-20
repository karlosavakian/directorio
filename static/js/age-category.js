function initAgeCategory(root = document) {
  const ageInput = root.querySelector('input[name="edad"]');
  const select = root.querySelector('select[name="modalidad"]');
  const tipoRadios = root.querySelectorAll('input[name="tipo_competidor"]');
  const modalidadField = select ? select.closest('.form-field') : null;
  if (!ageInput) return;

  const updateVisibility = () => {
    const checked = root.querySelector('input[name="tipo_competidor"]:checked');
    if (modalidadField) {
      modalidadField.style.display = checked && checked.value === 'amateur' ? '' : 'none';
    }
  };

  tipoRadios.forEach(r => r.addEventListener('change', updateVisibility));

  const update = () => {
    const age = parseInt(ageInput.value, 10);
    let type = '';
    let value = '';
    if (!isNaN(age)) {
      if (age >= 13 && age <= 14) {
        type = 'amateur';
        value = 'schoolboy';
      } else if (age >= 15 && age <= 16) {
        type = 'amateur';
        value = 'junior';
      } else if (age >= 17 && age <= 18) {
        type = 'amateur';
        value = 'joven';
      } else if (age >= 19 && age <= 40) {
        type = 'amateur';
        value = 'elite';
      } else if (age >= 41) {
        type = 'profesional';
        value = 'profesional';
      }
    }
    if (tipoRadios.length) {
      tipoRadios.forEach(r => {
        r.checked = r.value === type;
      });
    }
    if (select) {
      select.value = type === 'amateur' ? value : '';
      select.dispatchEvent(new Event('change'));
    }
    updateVisibility();
  };

  ageInput.addEventListener('input', update);
  update();
  updateVisibility();
}

document.addEventListener('DOMContentLoaded', () => {
  initAgeCategory();
});

window.initAgeCategory = initAgeCategory;
