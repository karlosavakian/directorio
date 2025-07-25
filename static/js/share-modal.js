// Generic share modal functionality for profile and club pages

document.addEventListener('DOMContentLoaded', () => {
  const modalEl = document.getElementById('shareProfileModal');
  if (!modalEl) return;

  const triggers = document.querySelectorAll('#profile-share, #club-share, .post-share');
  const copyBtn = modalEl.querySelector('.share-copy');
  const embedBtn = modalEl.querySelector('.share-embed');

  function setLinks() {
    const url = encodeURIComponent(window.location.href);
    const title = encodeURIComponent(document.title);
    modalEl.querySelector('#share-email').href = `mailto:?subject=${title}&body=${url}`;
    modalEl.querySelector('#share-whatsapp').href = `https://wa.me/?text=${title}%20${url}`;
    modalEl.querySelector('#share-messenger').href = `fb-messenger://share/?link=${url}`;
    modalEl.querySelector('#share-facebook').href = `https://www.facebook.com/sharer/sharer.php?u=${url}`;
    modalEl.querySelector('#share-instagram').href = `https://www.instagram.com/?url=${url}`;
    modalEl.querySelector('#share-telegram').href = `https://t.me/share/url?url=${url}&text=${title}`;
    modalEl.querySelector('#share-x').href = `https://twitter.com/intent/tweet?url=${url}&text=${title}`;
  }

  triggers.forEach(btn => {
    btn.addEventListener('click', () => {
      setLinks();
      new bootstrap.Modal(modalEl).show();
    });
  });

  if (copyBtn) {
    copyBtn.addEventListener('click', () => {
      navigator.clipboard.writeText(window.location.href);
      showToast('Enlace copiado');
    });
  }

  if (embedBtn) {
    embedBtn.addEventListener('click', () => {
      const embed = `<iframe src="${window.location.href}" width="600" height="400"></iframe>`;
      navigator.clipboard.writeText(embed);
      showToast('Código copiado');
    });
  }
});

function showToast(message) {
  let container = document.querySelector('.toast-container');
  if (!container) {
    container = document.createElement('div');
    container.className = 'toast-container position-fixed top-0 end-0 p-3';
    document.body.appendChild(container);
  }
  const toast = document.createElement('div');
  toast.className = 'toast bg-black text-bg-success border-0 mb-2';
  toast.role = 'alert';
  toast.innerHTML = `<div class="d-flex"><div class="toast-body">${message}</div>` +
                    `<button type="button" class="btn-close btn-close-white me-2 m-auto" data-bs-dismiss="toast" aria-label="Close"></button></div>`;
  container.appendChild(toast);
  new bootstrap.Toast(toast).show();
}
