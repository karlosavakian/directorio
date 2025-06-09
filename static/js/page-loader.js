document.addEventListener('DOMContentLoaded', () => {
    const loader = document.getElementById('loader');
    if (!loader) return;

    const hide = () => loader.classList.add('is-hidden');
    const show = () => loader.classList.remove('is-hidden');

    hide();
    window.addEventListener('load', hide);
    window.addEventListener('pageshow', hide);

    document.body.addEventListener('click', (e) => {
        const link = e.target.closest('a[href]');
        if (link && link.target !== '_blank' && !link.href.startsWith('#')) {
            show();
        }
    });

    document.body.addEventListener('submit', show, true);
    window.addEventListener('pagehide', show);
});
