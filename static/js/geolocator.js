document.addEventListener('DOMContentLoaded', function () {


    //geolocator
    const input = document.getElementById('search-input');
    const wrapper = document.querySelector('.autocomplete-wrapper');
    const locationOption = document.getElementById('use-location-option');
    const list = document.getElementById('autocomplete-list');

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

    const suggestions = Object.values(citiesByRegion).flat();

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
    

});
