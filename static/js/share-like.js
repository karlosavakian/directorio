document.addEventListener('DOMContentLoaded', () => {
  const heart = document.getElementById('club-heart');
  if (heart) {
    heart.addEventListener('click', async () => {
      const url = heart.dataset.url;
      const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;

      // Optimistic UI update
      heart.classList.toggle('liked');

      try {
        const res = await fetch(url, {
          method: 'POST',
          headers: { 'X-CSRFToken': csrftoken },
          credentials: 'same-origin'
        });
        if (res.redirected) {
          const modal = new bootstrap.Modal(document.getElementById('loginModal'));
          modal.show();
          heart.classList.toggle('liked'); // revert optimistic update
          return;
        }
        if (res.ok) {
          const data = await res.json();
          heart.classList.toggle('liked', data.following);
          if (data.message) {
            showToast(data.message);
          }
        } else {
          heart.classList.toggle('liked'); // revert on error
        }
      } catch (err) {
        console.error(err);
        heart.classList.toggle('liked'); // revert on error
      }
    });
  }

  const shareBtn = document.getElementById('club-share');
  if (shareBtn) {
    let menu = null;
    shareBtn.addEventListener('click', async () => {
      if (navigator.share) {
        try {
          await navigator.share({
            title: document.title,
            url: window.location.href
          });
        } catch (err) {
          console.error('Share failed:', err);
        }
        return;
      }

      if (!menu) {
        menu = document.createElement('div');
        menu.className = 'share-menu';
        const url = encodeURIComponent(window.location.href);
        const title = encodeURIComponent(document.title);
        menu.innerHTML = `
          <a href="https://www.facebook.com/sharer/sharer.php?u=${url}" target="_blank">Facebook</a>
          <a href="https://twitter.com/intent/tweet?url=${url}&text=${title}" target="_blank">Twitter</a>
          <a href="https://wa.me/?text=${url}" target="_blank">WhatsApp</a>
          <button type="button" class="copy-link">Copiar enlace</button>
          <a href="mailto:?subject=${title}&body=${url}">Email</a>
        `;
        shareBtn.parentElement.appendChild(menu);
        menu.querySelector('.copy-link').addEventListener('click', () => {
          navigator.clipboard.writeText(window.location.href);
          showToast('Enlace copiado');
        });
      }
      menu.classList.toggle('show');
    });

    document.addEventListener('click', (e) => {
      if (menu && !shareBtn.contains(e.target) && !menu.contains(e.target)) {
        menu.classList.remove('show');
      }
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
