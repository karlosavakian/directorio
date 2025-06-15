 document.addEventListener("DOMContentLoaded", function () {
    const dropdown = document.getElementById("category-dropdown");
    const selectedText = dropdown.querySelector(".selected-text");
    const hiddenInput = document.getElementById("category-input");
    const menu = document.getElementById("category-menu");
    const items = menu.querySelectorAll(".dropdown-item");

    // Mostrar u ocultar menú
    dropdown.addEventListener("click", function (e) {
        e.stopPropagation();
        dropdown.classList.toggle("active");
        menu.style.display = menu.style.display === "block" ? "none" : "block";
    });

    // Seleccionar opción
    items.forEach(item => {
        item.addEventListener("click", function (e) {
            e.stopPropagation();
            selectedText.textContent = item.textContent;
            hiddenInput.value = item.dataset.value;
            menu.style.display = "none";
            dropdown.classList.remove("active"); // cierra flecha animada
        });
    });

    // Cerrar menú al hacer click fuera
    document.addEventListener("click", function (e) {
        if (!dropdown.contains(e.target)) {
            menu.style.display = "none";
            dropdown.classList.remove("active");
        }
    });


});
 
