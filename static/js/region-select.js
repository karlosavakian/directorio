const SPANISH_REGIONS = [
  "Andalucía", "Aragón", "Asturias", "Islas Baleares", "Canarias", "Cantabria",
  "Castilla-La Mancha", "Castilla y León", "Cataluña", "Comunidad Valenciana",
  "Extremadura", "Galicia", "La Rioja", "Comunidad de Madrid", "Región de Murcia",
  "Navarra", "País Vasco", "Ceuta", "Melilla"
];

let REGION_DATA = {}; // Aquí se cargará el JSON

function initRegionSelect() {
  const country = document.getElementById('id_country');
  const regionFieldWrapper = document.getElementById('id_region')?.closest('.form-field');
  const provinceSelect = document.getElementById('id_province');
  const citySelect = document.getElementById('id_city');

  if (!country || !regionFieldWrapper) return;

  // Paso 1: Carga el JSON con comunidades, provincias y ciudades
  fetch('/static/data/cp_provincias_poblaciones.json')
    .then(res => res.json())
    .then(data => {
      REGION_DATA = data;
      init();
    });

  function buildSelect(options = [], name = '', value = '') {
    const select = document.createElement('select');
    select.name = name;
    select.id = `id_${name}`;
    select.className = 'form-control';

    const empty = document.createElement('option');
    empty.value = '';
    empty.textContent = `Selecciona ${name}`;
    select.appendChild(empty);

    options.forEach(opt => {
      const o = document.createElement('option');
      o.value = opt;
      o.textContent = opt;
      select.appendChild(o);
    });

    select.value = value;
    return select;
  }

  function buildInput(value = '', name = 'region') {
    const input = document.createElement('input');
    input.type = 'text';
    input.name = name;
    input.id = `id_${name}`;
    input.className = 'form-control';
    input.value = value;
    return input;
  }

  function updateField() {
    let current = regionFieldWrapper.querySelector('#id_region');
    const clearBtn = regionFieldWrapper.querySelector('.clear-btn');

    if (country.value === 'España') {
      if (current.tagName.toLowerCase() !== 'select') {
        const select = buildSelect(SPANISH_REGIONS, 'region', current.value);
        current.replaceWith(select);
        if (clearBtn) clearBtn.style.display = 'none';
        if (window.initSelectLabels) window.initSelectLabels(regionFieldWrapper);
        current = select;
      }

      current.addEventListener('change', () => {
        updateProvince(current.value);
      });

      updateProvince(current.value); // Inicializa provincias si ya había región seleccionada
    } else {
      if (current.tagName.toLowerCase() !== 'input') {
        const input = buildInput('');
        current.replaceWith(input);
        if (clearBtn) {
          clearBtn.style.display = 'none';
          clearBtn.onclick = () => {
            input.value = '';
            input.dispatchEvent(new Event('input', { bubbles: true }));
            clearBtn.style.display = 'none';
            input.focus();
          };
          const toggle = () => {
            if (document.activeElement === input && input.value) {
              clearBtn.style.display = 'block';
            } else {
              clearBtn.style.display = 'none';
            }
          };
          input.addEventListener('focus', toggle);
          input.addEventListener('blur', toggle);
          input.addEventListener('input', toggle);
          toggle();
        }
      }

      provinceSelect.innerHTML = `<option value="">Selecciona una provincia</option>`;
      citySelect.innerHTML = `<option value="">Selecciona una ciudad</option>`;
      provinceSelect.disabled = true;
      citySelect.disabled = true;
    }
  }

  function updateProvince(region) {
    provinceSelect.innerHTML = `<option value="">Selecciona una provincia</option>`;
    citySelect.innerHTML = `<option value="">Selecciona una ciudad</option>`;
    citySelect.disabled = true;

    if (!region || !REGION_DATA[region]) {
      provinceSelect.disabled = true;
      return;
    }

    const provincias = Object.keys(REGION_DATA[region]);
    provincias.forEach(p => {
      const opt = new Option(p, p);
      provinceSelect.appendChild(opt);
    });

    provinceSelect.disabled = false;

    provinceSelect.addEventListener('change', () => {
      updateCity(region, provinceSelect.value);
    });
  }

  function updateCity(region, provincia) {
    citySelect.innerHTML = `<option value="">Selecciona una ciudad</option>`;
    if (!region || !provincia || !REGION_DATA[region][provincia]) {
      citySelect.disabled = true;
      return;
    }

    const ciudades = REGION_DATA[region][provincia];
    ciudades.forEach(c => {
      const opt = new Option(c, c);
      citySelect.appendChild(opt);
    });

    citySelect.disabled = false;
  }

  function init() {
    country.addEventListener('change', updateField);
    updateField();
  }
}

document.addEventListener('DOMContentLoaded', initRegionSelect);
