document.addEventListener('DOMContentLoaded', function () {
    const loader = document.getElementById('loader');
    if (!loader) return;
    setTimeout(() => {
        loader.classList.add('hidden');
    }, 300);
});

window.addEventListener('beforeunload', function () {
    const loader = document.getElementById('loader');
    if (loader) {
        loader.classList.remove('hidden');
    }
});
