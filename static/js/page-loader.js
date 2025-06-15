document.addEventListener('DOMContentLoaded', function () {
    const loader = document.getElementById('loader');
    if (!loader) return;
    setTimeout(() => {
        loader.classList.add('hidden');
    }, 300);
});

// When navigating back using the browser's history the page might be
// restored from the bfcache and `DOMContentLoaded` will not fire again.
// Listen to the `pageshow` event so the loader can be hidden in that case.
window.addEventListener('pageshow', function () {
    const loader = document.getElementById('loader');
    if (loader) {
        loader.classList.add('hidden');
    }
});

window.addEventListener('beforeunload', function () {
    const loader = document.getElementById('loader');
    if (loader) {
        loader.classList.remove('hidden');
    }
});

// Clean up lingering Bootstrap modal overlays when a modal is fully hidden
document.addEventListener('hidden.bs.modal', function () {
    if (!document.querySelector('.modal.show')) {
        document.querySelectorAll('.modal-backdrop').forEach(b => b.remove());
        document.body.classList.remove('modal-open');
        document.body.style.removeProperty('padding-right');
    }
});