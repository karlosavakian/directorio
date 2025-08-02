document.addEventListener("DOMContentLoaded", function () {
    const dropdown = document.getElementById("user-dropdown");
    if (!dropdown) return;
    const menu = document.getElementById("user-menu");
    const burger = document.getElementById("burger-button");
    const overlay = document.getElementById("sidebar-overlay");
    const closeBtn = document.getElementById("menu-close-button");

    function toggleMenu(e) {
        e.stopPropagation();
        dropdown.classList.toggle("active");
        if (window.innerWidth <= 991) {
            menu.classList.toggle("open");
            if (overlay) overlay.classList.toggle("show");
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
    if (overlay)
        overlay.addEventListener("click", function () {
            menu.classList.remove("open");
            dropdown.classList.remove("active");
            overlay.classList.remove("show");
        });
    if (closeBtn)
        closeBtn.addEventListener("click", function (e) {
            e.stopPropagation();
            menu.classList.remove("open");
            dropdown.classList.remove("active");
            if (overlay) overlay.classList.remove("show");
        });

    document.addEventListener("click", function (e) {
        if (!dropdown.contains(e.target) && e.target !== burger) {
            if (window.innerWidth <= 991) {
                menu.classList.remove("open");
                if (overlay) overlay.classList.remove("show");
            } else {
                menu.style.display = "none";
            }
            dropdown.classList.remove("active");
        }
    });
});
