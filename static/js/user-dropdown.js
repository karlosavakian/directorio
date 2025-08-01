document.addEventListener("DOMContentLoaded", function () {
    const dropdown = document.getElementById("user-dropdown");
    if (!dropdown) return;
    const menu = document.getElementById("user-menu");
    const burger = document.getElementById("burger-button");

    function toggleMenu(e) {
        e.stopPropagation();
        dropdown.classList.toggle("active");
        menu.style.display = menu.style.display === "block" ? "none" : "block";
    }

    dropdown.addEventListener("click", toggleMenu);
    if (burger) burger.addEventListener("click", toggleMenu);

    document.addEventListener("click", function (e) {
        if (!dropdown.contains(e.target) && e.target !== burger) {
            menu.style.display = "none";
            dropdown.classList.remove("active");
        }
    });
 });
