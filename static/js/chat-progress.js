document.addEventListener('DOMContentLoaded', function () {
    const bar = document.getElementById('chat-progress-bar');
    if (!bar) return;
    requestAnimationFrame(() => {
        bar.style.width = '100%';
    });
    bar.addEventListener('transitionend', () => {
        bar.style.opacity = '0';
    });
});

window.addEventListener('beforeunload', function () {
    const bar = document.getElementById('chat-progress-bar');
    if (!bar) return;
    bar.style.opacity = '1';
    bar.style.width = '0';
});
