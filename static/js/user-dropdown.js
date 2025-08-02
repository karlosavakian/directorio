document.addEventListener("DOMContentLoaded", function () {
    const dropdown = document.getElementById("user-dropdown");
    if (!dropdown) return;
    const menu = document.getElementById("user-menu");
    const burger = document.getElementById("burger-button");

    function toggleMenu(e) {
        e.stopPropagation();
        dropdown.classList.toggle("active");
        if (window.innerWidth <= 991) {
            menu.classList.toggle("open");
        } else {
            menu.style.display =
                menu.style.display === "block" ? "none" : "block";
        }
    }

    dropdown.addEventListener("click", function (e) {
        if (window.innerWidth > 991) {
            toggleMenu(e);
        }
    });
    if (burger) burger.addEventListener("click", toggleMenu);

    document.addEventListener("click", function (e) {
        if (!dropdown.contains(e.target) && e.target !== burger) {
            if (window.innerWidth <= 991) {
                menu.classList.remove("open");
            } else {
                menu.style.display = "none";
            }
            dropdown.classList.remove("active");
        }
    });
});
