document.addEventListener('DOMContentLoaded', () => {
    const loader = document.getElementById('loader');
    if (!loader) return;

    const hide = () => loader.classList.add('is-hidden');
    const show = () => loader.classList.remove('is-hidden');

    hide();

    // Asegura que el loader se oculte al cargar la página normalmente
    window.addEventListener('load', hide);

    // Asegura que el loader se oculte si la página se recupera de la caché (bfcache)
    window.addEventListener('pageshow', (event) => {
        if (event.persisted) {
            hide();
        } else {
            hide();
        }
    });

    // Muestra el loader al hacer clic en enlaces (salvo externos o anclas)
    document.body.addEventListener('click', (e) => {
        const link = e.target.closest('a[href]');
        if (link && link.target !== '_blank' && !link.href.startsWith('#')) {
            show();
        }
    });

    // Muestra el loader al enviar formularios
    document.body.addEventListener('submit', show, true);

    // Evita que el loader se quede atascado al retroceder usando el historial
    window.addEventListener('beforeunload', show);
});
