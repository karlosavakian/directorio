document.addEventListener("DOMContentLoaded", function () {
    const dropdown = document.getElementById("category-dropdown");
    const selectedText = dropdown.querySelector(".selected-text");
    const hiddenInput = document.getElementById("category-input");
    const items = dropdown.querySelectorAll(".dropdown-item");

    dropdown.querySelector(".selected").addEventListener("click", () => {
        const menu = dropdown.querySelector(".dropdown-menu");
        menu.style.display = menu.style.display === "block" ? "none" : "block";
    });

    items.forEach(item => {
        item.addEventListener("click", () => {
            selectedText.textContent = item.textContent;
            hiddenInput.value = item.dataset.value;
            dropdown.querySelector(".dropdown-menu").style.display = "none";
        });
    });

    document.addEventListener("click", function (e) {
        if (!dropdown.contains(e.target)) {
            dropdown.querySelector(".dropdown-menu").style.display = "none";
        }
    });
});
