document.addEventListener('DOMContentLoaded', function () {
    const loader = document.getElementById('loader');
    if (!loader) return;
    setTimeout(() => {
        loader.classList.add('hidden');
    }, 300);
});

// Ensure the loader is hidden when navigating back from bfcache
window.addEventListener('pageshow', function (event) {
    const loader = document.getElementById('loader');
    if (loader && event.persisted) {
        loader.classList.add('hidden');
    }
});

window.addEventListener('beforeunload', function () {
    const loader = document.getElementById('loader');
    if (loader) {
        loader.classList.remove('hidden');
    }
});
