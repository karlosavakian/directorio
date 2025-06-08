document.addEventListener('DOMContentLoaded', function() {
    const header = document.querySelector('header.navbar');
    if (!header) return;

    const initialHeight = header.offsetHeight;
    const scrolledHeight = initialHeight - 10;
    header.style.height = initialHeight + 'px';

    window.addEventListener('scroll', function() {
        if (window.scrollY > 0) {
            header.style.height = scrolledHeight + 'px';
        } else {
            header.style.height = initialHeight + 'px';
        }
    });
});

