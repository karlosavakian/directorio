const SPANISH_REGIONS = [
  "Andalucía",
  "Aragón",
  "Asturias",
  "Islas Baleares",
  "Canarias",
  "Cantabria",
  "Castilla-La Mancha",
  "Castilla y León",
  "Cataluña",
  "Comunidad Valenciana",
  "Extremadura",
  "Galicia",
  "La Rioja",
  "Comunidad de Madrid",
  "Región de Murcia",
  "Navarra",
  "País Vasco",
  "Ceuta",
  "Melilla"
];

function initRegionSelect() {
  const country = document.getElementById('id_country');
  const regionFieldWrapper = document.getElementById('id_region')?.closest('.form-field');
  if (!country || !regionFieldWrapper) return;

  const buildSelect = (value = '') => {
    const select = document.createElement('select');
    select.name = 'region';
    select.id = 'id_region';
    select.className = 'form-control';
    const empty = document.createElement('option');
    empty.value = '';
    select.appendChild(empty);
    SPANISH_REGIONS.forEach((r) => {
      const opt = document.createElement('option');
      opt.value = r;
      opt.textContent = r;
      select.appendChild(opt);
    });
    select.value = value;
    return select;
  };

  const buildInput = (value = '') => {
    const input = document.createElement('input');
    input.type = 'text';
    input.name = 'region';
    input.id = 'id_region';
    input.className = 'form-control';
    input.value = value;
    return input;
  };

  const updateField = () => {
    let current = regionFieldWrapper.querySelector('#id_region');
    const clearBtn = regionFieldWrapper.querySelector('.clear-btn');
    if (country.value === 'España') {
      if (current.tagName.toLowerCase() !== 'select') {
        const select = buildSelect(current.value);
        current.replaceWith(select);
        if (clearBtn) clearBtn.style.display = 'none';
        if (window.initSelectLabels) window.initSelectLabels(regionFieldWrapper);
      }
    } else {
      if (current.tagName.toLowerCase() !== 'input') {
        const input = buildInput('');
        current.replaceWith(input);
        if (clearBtn) {
          clearBtn.style.display = '';
          clearBtn.onclick = () => {
            input.value = '';
            input.dispatchEvent(new Event('input', { bubbles: true }));
            clearBtn.style.display = 'none';
            input.focus();
          };
          input.addEventListener('input', () => {
            clearBtn.style.display = input.value ? 'block' : 'none';
          });
          clearBtn.style.display = input.value ? 'block' : 'none';
        }
      }
    }
  };

  country.addEventListener('change', updateField);
  updateField();
}

document.addEventListener('DOMContentLoaded', initRegionSelect);
