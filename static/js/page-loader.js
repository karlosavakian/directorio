function hideLoader() {
    const loader = document.getElementById('loader');
    if (loader) {
        loader.classList.add('hidden');
    }
}

document.addEventListener('DOMContentLoaded', hideLoader);
window.addEventListener('load', hideLoader);
window.addEventListener('pageshow', hideLoader);

window.addEventListener('beforeunload', function () {
    const loader = document.getElementById('loader');
    if (loader) {
        loader.classList.remove('hidden');
    }
});
