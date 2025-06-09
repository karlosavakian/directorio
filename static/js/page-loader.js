function hideLoader() {
    const loader = document.getElementById('loader');
    if (loader) {
        loader.classList.add('hidden');
    }
}

document.addEventListener('DOMContentLoaded', hideLoader);
window.addEventListener('load', hideLoader);
window.addEventListener('pageshow', hideLoader);

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
