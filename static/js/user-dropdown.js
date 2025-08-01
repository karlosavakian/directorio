document.addEventListener("DOMContentLoaded", function () {
    const dropdown = document.getElementById("user-dropdown");
    if (!dropdown) return;
    const menu = document.getElementById("user-menu");
    const overlay = document.getElementById("dropdown-overlay");

    dropdown.addEventListener("click", function (e) {
        e.stopPropagation();
        dropdown.classList.toggle("active");
        const isOpen = menu.style.display === "block";
        menu.style.display = isOpen ? "none" : "block";
        if (overlay) {
            overlay.classList.toggle("show", !isOpen);
        }
    });

    if (overlay) {
        overlay.addEventListener("click", function () {
            menu.style.display = "none";
            dropdown.classList.remove("active");
            overlay.classList.remove("show");
        });
    }

    document.addEventListener("click", function (e) {
        if (!dropdown.contains(e.target)) {
            menu.style.display = "none";
            dropdown.classList.remove("active");
            if (overlay) {
                overlay.classList.remove("show");
            }
        }
    });
});
