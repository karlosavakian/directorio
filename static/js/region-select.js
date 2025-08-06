let REGION_DATA = {};
let SPANISH_REGIONS = [];

function initRegionSelect() {
  const country = document.getElementById('id_country');
  const regionFieldWrapper = document.getElementById('id_region')?.closest('.form-field');
  let provinceSelect = document.getElementById('id_province');
  let citySelect = document.getElementById('id_city');
  const provinceWrapper = provinceSelect?.closest('.form-field');
  const cityWrapper = citySelect?.closest('.form-field');

  if (!country || !regionFieldWrapper || !provinceSelect || !citySelect) return;

  fetch('/static/data/arbol.json')
    .then(res => res.json())
    .then(data => {
      data.forEach(r => {
        REGION_DATA[r.label] = {};
        r.provinces.forEach(p => {
          REGION_DATA[r.label][p.label] = p.towns.map(t => t.label);
        });
      });
      SPANISH_REGIONS = Object.keys(REGION_DATA);
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
        select.options[0].textContent = 'Selecciona una comunidad autónoma';
        current.replaceWith(select);
        if (clearBtn) clearBtn.style.display = 'none';
        if (window.initSelectLabels) window.initSelectLabels(regionFieldWrapper);
        current = select;
      }

      if (provinceSelect.tagName.toLowerCase() !== 'select') {
        const select = buildSelect([], 'province', '');
        select.options[0].textContent = 'Selecciona una provincia';
        provinceSelect.replaceWith(select);
        if (window.initSelectLabels && provinceWrapper) window.initSelectLabels(provinceWrapper);
        provinceSelect = select;
      } else {
        provinceSelect.innerHTML = `<option value="">Selecciona una provincia</option>`;
      }

      if (citySelect.tagName.toLowerCase() !== 'select') {
        const select = buildSelect([], 'city', '');
        select.options[0].textContent = 'Selecciona una ciudad';
        citySelect.replaceWith(select);
        if (window.initSelectLabels && cityWrapper) window.initSelectLabels(cityWrapper);
        citySelect = select;
      } else {
        citySelect.innerHTML = `<option value="">Selecciona una ciudad</option>`;
      }

      current.addEventListener('change', () => {
        updateProvince(current.value);
      });

      updateProvince(current.value);
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
        current = input;
      }

      if (provinceSelect.tagName.toLowerCase() !== 'input') {
        const input = buildInput('', 'province');
        provinceSelect.replaceWith(input);
        if (window.initSelectLabels && provinceWrapper) window.initSelectLabels(provinceWrapper);
        provinceSelect = input;
      } else {
        provinceSelect.value = '';
      }

      if (citySelect.tagName.toLowerCase() !== 'input') {
        const input = buildInput('', 'city');
        citySelect.replaceWith(input);
        if (window.initSelectLabels && cityWrapper) window.initSelectLabels(cityWrapper);
        citySelect = input;
      } else {
        citySelect.value = '';
      }
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

