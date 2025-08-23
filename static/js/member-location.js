// Handles dependent dropdown for region and city in member forms
function initMemberLocationSelects(root = document) {
  const region =
    root.querySelector('#id_region') ||
    root.querySelector('#id_comunidad_autonoma');
  const city =
    root.querySelector('#id_localidad') ||
    root.querySelector('#id_ciudad');
  if (!region || !city) return;

  const citiesByRegion = {
    'Andalucía': ['Almería', 'Cádiz', 'Córdoba', 'Granada', 'Huelva', 'Jaén', 'Málaga', 'Sevilla'],
    'Aragón': ['Huesca', 'Teruel', 'Zaragoza'],
    'Asturias': ['Oviedo'],
    'Islas Baleares': ['Palma de Mallorca'],
    'Canarias': ['Las Palmas de Gran Canaria', 'Santa Cruz de Tenerife'],
    'Cantabria': ['Santander'],
    'Castilla-La Mancha': ['Albacete', 'Ciudad Real', 'Cuenca', 'Guadalajara', 'Toledo'],
    'Castilla y León': ['Ávila', 'Burgos', 'León', 'Palencia', 'Salamanca', 'Segovia', 'Soria', 'Valladolid', 'Zamora'],
    'Cataluña': ['Barcelona', 'Girona', 'Lleida', 'Tarragona'],
    'Comunidad Valenciana': ['Alicante', 'Castellón de la Plana', 'Valencia'],
    'Extremadura': ['Badajoz', 'Cáceres'],
    'Galicia': ['A Coruña', 'Lugo', 'Ourense', 'Pontevedra'],
    'Madrid': ['Madrid'],
    'Murcia': ['Murcia'],
    'Navarra': ['Pamplona'],
    'País Vasco': ['Vitoria-Gasteiz', 'San Sebastián', 'Bilbao'],
    'La Rioja': ['Logroño'],
    'Ceuta': ['Ceuta'],
    'Melilla': ['Melilla']
  };

  const cityInitial = city.value;
  if (cityInitial) city.dataset.initial = cityInitial;

  function clearOptions(select) {
    select.innerHTML = '<option value=""></option>';
  }

  function populateCityOptions(options) {
    const currentCity = city.dataset.initial || city.value;
    clearOptions(city);
    options.forEach(function (c) {
      const opt = document.createElement('option');
      opt.value = c;
      opt.textContent = c;
      city.appendChild(opt);
    });
    city.disabled = options.length === 0;
    if (options.includes(currentCity)) {
      city.value = currentCity;
    }
    city.dataset.initial = '';
  }

  function updateCitiesForRegion() {
    const selectedRegion = region.value;
    const options = citiesByRegion[selectedRegion] || [];
    populateCityOptions(options);
  }

  region.addEventListener('change', updateCitiesForRegion);
  updateCitiesForRegion();
}

document.addEventListener('DOMContentLoaded', function () {
  initMemberLocationSelects();
});

window.initMemberLocationSelects = initMemberLocationSelects;
