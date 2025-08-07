// Handles dependent dropdowns for country/region/province/city in the club dashboard

document.addEventListener('DOMContentLoaded', function () {
  const country = document.getElementById('id_country');
  const region = document.getElementById('id_region');
  const province = document.getElementById('id_province');
  const city = document.getElementById('id_city');

  if (!country || !region || !province || !city) return;

  const provincesByRegion = {
    'Andalucía': ['Almería', 'Cádiz', 'Córdoba', 'Granada', 'Huelva', 'Jaén', 'Málaga', 'Sevilla'],
    'Aragón': ['Huesca', 'Teruel', 'Zaragoza'],
    'Asturias': ['Asturias'],
    'Islas Baleares': ['Islas Baleares'],
    'Canarias': ['Las Palmas', 'Santa Cruz de Tenerife'],
    'Cantabria': ['Cantabria'],
    'Castilla-La Mancha': ['Albacete', 'Ciudad Real', 'Cuenca', 'Guadalajara', 'Toledo'],
    'Castilla y León': ['Ávila', 'Burgos', 'León', 'Palencia', 'Salamanca', 'Segovia', 'Soria', 'Valladolid', 'Zamora'],
    'Cataluña': ['Barcelona', 'Girona', 'Lérida', 'Tarragona'],
    'Comunidad Valenciana': ['Alicante', 'Castellón', 'Valencia'],
    'Extremadura': ['Badajoz', 'Cáceres'],
    'Galicia': ['La Coruña', 'Lugo', 'Orense', 'Pontevedra'],
    'Madrid': ['Madrid'],
    'Murcia': ['Murcia'],
    'Navarra': ['Navarra'],
    'País Vasco': ['Álava', 'Guipúzcoa', 'Vizcaya'],
    'La Rioja': ['La Rioja'],
    'Ceuta': ['Ceuta'],
    'Melilla': ['Melilla']
  };

  const citiesByProvince = {
    'Álava': ['Vitoria-Gasteiz'],
    'Albacete': ['Albacete'],
    'Alicante': ['Alicante'],
    'Almería': ['Almería'],
    'Asturias': ['Oviedo'],
    'Ávila': ['Ávila'],
    'Badajoz': ['Badajoz'],
    'Barcelona': ['Barcelona'],
    'Burgos': ['Burgos'],
    'Cáceres': ['Cáceres'],
    'Cádiz': ['Cádiz'],
    'Cantabria': ['Santander'],
    'Castellón': ['Castellón de la Plana'],
    'Ciudad Real': ['Ciudad Real'],
    'Córdoba': ['Córdoba'],
    'Cuenca': ['Cuenca'],
    'Girona': ['Girona'],
    'Granada': ['Granada'],
    'Guadalajara': ['Guadalajara'],
    'Guipúzcoa': ['San Sebastián'],
    'Huelva': ['Huelva'],
    'Huesca': ['Huesca'],
    'Islas Baleares': ['Palma de Mallorca'],
    'Jaén': ['Jaén'],
    'La Coruña': ['A Coruña'],
    'La Rioja': ['Logroño'],
    'Las Palmas': ['Las Palmas de Gran Canaria'],
    'León': ['León'],
    'Lérida': ['Lleida'],
    'Lugo': ['Lugo'],
    'Madrid': ['Madrid'],
    'Málaga': ['Málaga'],
    'Murcia': ['Murcia'],
    'Navarra': ['Pamplona'],
    'Orense': ['Ourense'],
    'Palencia': ['Palencia'],
    'Pontevedra': ['Pontevedra'],
    'Salamanca': ['Salamanca'],
    'Santa Cruz de Tenerife': ['Santa Cruz de Tenerife'],
    'Segovia': ['Segovia'],
    'Sevilla': ['Sevilla'],
    'Soria': ['Soria'],
    'Tarragona': ['Tarragona'],
    'Teruel': ['Teruel'],
    'Toledo': ['Toledo'],
    'Valencia': ['Valencia'],
    'Valladolid': ['Valladolid'],
    'Vizcaya': ['Bilbao'],
    'Zamora': ['Zamora'],
    'Zaragoza': ['Zaragoza'],
    'Ceuta': ['Ceuta'],
    'Melilla': ['Melilla']
  };

  const provinceInitial = province.value;
  const cityInitial = city.value;
  if (provinceInitial) province.dataset.initial = provinceInitial;
  if (cityInitial) city.dataset.initial = cityInitial;

  function clearOptions(select) {
    select.innerHTML = '<option value=""></option>';
  }

  function updateCities() {
    const selectedProvince = province.value;
    const currentCity = city.dataset.initial || city.value;
    clearOptions(city);
    if (selectedProvince && citiesByProvince[selectedProvince]) {
      citiesByProvince[selectedProvince].forEach(function (c) {
        const opt = document.createElement('option');
        opt.value = c;
        opt.textContent = c;
        city.appendChild(opt);
      });
      city.disabled = false;
      if (citiesByProvince[selectedProvince].includes(currentCity)) {
        city.value = currentCity;
      }
    } else {
      city.disabled = true;
    }
    city.dataset.initial = '';
  }

  function updateProvinces() {
    const selectedRegion = region.value;
    const currentProvince = province.dataset.initial || province.value;
    clearOptions(province);
    clearOptions(city);
    if (selectedRegion && provincesByRegion[selectedRegion]) {
      provincesByRegion[selectedRegion].forEach(function (p) {
        const opt = document.createElement('option');
        opt.value = p;
        opt.textContent = p;
        province.appendChild(opt);
      });
      province.disabled = false;
      if (provincesByRegion[selectedRegion].includes(currentProvince)) {
        province.value = currentProvince;
      }
    } else {
      province.disabled = true;
      city.disabled = true;
    }
    province.dataset.initial = '';
    updateCities();
  }

  function updateByCountry() {
    if (country.value === 'España') {
      region.parentElement.style.display = '';
      province.parentElement.style.display = '';
      region.disabled = false;
      updateProvinces();
    } else {
      region.parentElement.style.display = 'none';
      province.parentElement.style.display = 'none';
      province.disabled = true;
      city.disabled = false;
      clearOptions(province);
      clearOptions(city);
    }
  }

  country.addEventListener('change', updateByCountry);
  region.addEventListener('change', updateProvinces);
  province.addEventListener('change', updateCities);

  updateByCountry();
});

