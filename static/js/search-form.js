 
document.addEventListener("DOMContentLoaded", function () {
    const form = document.getElementById("main-search-form");
    const input = document.getElementById("search-input");

    // ✅ INPUT: animación al enfocar
    input.addEventListener("focus", () => input.classList.add("expanded"));
    input.addEventListener("blur", () => {
        if (input.value.trim() === "") input.classList.remove("expanded");
    });

    // ✅ VALIDACIÓN al enviar
    const stopWords = ["a", "de", "la", "el", "en", "y"];
    form.addEventListener("submit", function (e) {
        const text = input.value.trim().toLowerCase();
        const isValid = text.length >= 3 && !stopWords.includes(text);

        if (!isValid) {
            e.preventDefault();
            form.classList.add("form-error");
            setTimeout(() => form.classList.remove("form-error"), 600);
        }
    });

    // ✅ DROPDOWN personalizado
    const dropdown = document.getElementById("category-dropdown");
    const selectedText = dropdown.querySelector(".selected-text");
    const hiddenInput = document.getElementById("category-input");
    const menu = document.getElementById("category-menu");
    const items = menu.querySelectorAll(".dropdown-item");

    // Toggle menú
    dropdown.addEventListener("click", function (e) {
        e.stopPropagation();
        const visible = menu.style.display === "block";
        menu.style.display = visible ? "none" : "block";
        dropdown.classList.toggle("active", !visible);
    });

    // Selección de opción
    items.forEach(item => {
        item.addEventListener("click", function (e) {
            e.stopPropagation();
            selectedText.textContent = item.textContent;
            hiddenInput.value = item.dataset.value;
            menu.style.display = "none";
            dropdown.classList.remove("active");
        });
    });

    // Cierra menú si haces clic fuera
    document.addEventListener("click", function (e) {
        if (!dropdown.contains(e.target)) {
            menu.style.display = "none";
            dropdown.classList.remove("active");
        }
    });
}); 