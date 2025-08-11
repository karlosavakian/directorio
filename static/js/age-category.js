function initAgeCategory(root = document) {
  const birthInput = root.querySelector('input[name="fecha_nacimiento"]');
  const modalidadSelect = root.querySelector('select[name="modalidad"]');
  const tipoSelect = root.querySelector('select[name="tipo_competidor"]');
  const modalidadField = modalidadSelect ? modalidadSelect.closest('.form-field') : null;
  if (!birthInput) return;

  const updateVisibility = () => {
    const value = tipoSelect ? tipoSelect.value : '';
    if (modalidadField) {
      modalidadField.style.display = value === 'amateur' ? '' : 'none';
    }
  };

  if (tipoSelect) {
    tipoSelect.addEventListener('change', updateVisibility);
  }

  const getAge = () => {
    const val = birthInput.value;
    if (!val) return NaN;
    const d = new Date(val);
    const today = new Date();
    let age = today.getFullYear() - d.getFullYear();
    const m = today.getMonth() - d.getMonth();
    if (m < 0 || (m === 0 && today.getDate() < d.getDate())) {
      age--;
    }
    return age;
  };

  const update = () => {
    const age = getAge();
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
    if (tipoSelect) {
      tipoSelect.value = type;
      tipoSelect.dispatchEvent(new Event('change'));
    }
    if (modalidadSelect) {
      modalidadSelect.value = type === 'amateur' ? value : '';
      modalidadSelect.dispatchEvent(new Event('change'));
    }
    updateVisibility();
  };

  birthInput.addEventListener('change', update);
  update();
  updateVisibility();
}

document.addEventListener('DOMContentLoaded', () => {
  initAgeCategory();
});

window.initAgeCategory = initAgeCategory;
