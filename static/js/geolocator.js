document.addEventListener('DOMContentLoaded', function () {


    //geolocator
    const input = document.getElementById('search-input');
    const wrapper = document.querySelector('.autocomplete-wrapper');
    const locationOption = document.getElementById('use-location-option');
    const list = document.getElementById('autocomplete-list');

    const suggestions = [
        "A Coruña", "Álava", "Albacete", "Alicante", "Almería", "Asturias", "Ávila", "Badajoz", "Baleares", "Barcelona",
        "Burgos", "Cáceres", "Cádiz", "Cantabria", "Castellón", "Ciudad Real", "Córdoba", "Cuenca", "Girona", "Granada",
        "Guadalajara", "Gipuzkoa", "Huelva", "Huesca", "Jaén", "La Rioja", "Las Palmas", "León", "Lérida", "Lugo", "Madrid",
        "Málaga", "Murcia", "Navarra", "Ourense", "Palencia", "Pontevedra", "Salamanca", "Segovia", "Sevilla", "Soria",
        "Tarragona", "Santa Cruz de Tenerife", "Teruel", "Toledo", "Valencia", "Valladolid", "Vizcaya", "Zamora", "Zaragoza",
        "Ceuta", "Melilla"
    ];

    function showSuggestions(query) {
        list.innerHTML = ''; // Limpiar lista

        if (query.length === 0) {
            // No mostrar ciudades si no escribe nada
            return;
        }

        const matches = suggestions.filter(city => city.toLowerCase().startsWith(query));

        matches.forEach(match => {
            const li = document.createElement('li');
            li.textContent = match;
            li.addEventListener('click', () => {
                input.value = match;
                wrapper.style.display = 'none';
            });
            list.appendChild(li);
        });
    }

    // Abrir dropdown al hacer click en el input
    input.addEventListener('focus', () => {
        wrapper.style.display = 'block';
        list.innerHTML = ''; // Aseguramos que no haya ciudades si no escribe
    });

    // Al escribir
    input.addEventListener('input', () => {
        const query = input.value.trim().toLowerCase();
        list.innerHTML = '';
        showSuggestions(query);
    });

    // Cerrar dropdown si mueve el mouse fuera del wrapper
    wrapper.addEventListener('mouseleave', () => {
        wrapper.style.display = 'none';
    });



    // Geolocalización al click
    locationOption.addEventListener('click', () => {
        if (navigator.geolocation) {
            navigator.geolocation.getCurrentPosition(async (position) => {
                const lat = position.coords.latitude;
                const lon = position.coords.longitude;

                try {
                    const response = await fetch(`https://nominatim.openstreetmap.org/reverse?format=json&lat=${lat}&lon=${lon}`);
                    const data = await response.json();
                    const city = data.address.city || data.address.town || data.address.village || '';

                    input.value = city;
                } catch (err) {
                    console.error('Error obteniendo ciudad:', err);
                    input.value = `${lat.toFixed(4)}, ${lon.toFixed(4)}`;
                }

                wrapper.style.display = 'none';
            }, () => {
                alert("No se pudo obtener tu ubicación.");
                wrapper.style.display = 'none';
            });
        } else {
            alert("Geolocalización no soportada en este navegador.");
            wrapper.style.display = 'none';
        }
    });

    // Prevent empty searches
    const form = document.getElementById('main-search-form');
    if (form && input) {
        form.addEventListener('submit', function (e) {
            if (input.value.trim() === '') {
                e.preventDefault();
                input.classList.add('input-alert');
                input.focus();
            }
        });

        input.addEventListener('input', function () {
            if (input.value.trim() !== '') {
                input.classList.remove('input-alert');
            }
        });
    }

});
