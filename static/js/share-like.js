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
          headers: {
            'X-CSRFToken': csrftoken,
            'X-Requested-With': 'XMLHttpRequest'
          },
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
    shareBtn.addEventListener('click', () => {
      const modalEl = document.getElementById('shareProfileModal');
      if (modalEl) {
        const url = encodeURIComponent(window.location.href);
        const title = encodeURIComponent(document.title);
        modalEl.querySelector('#share-email').href = `mailto:?subject=${title}&body=${url}`;
        modalEl.querySelector('#share-whatsapp').href = `https://wa.me/?text=${title}%20${url}`;
        modalEl.querySelector('#share-messenger').href = `fb-messenger://share/?link=${url}`;
        modalEl.querySelector('#share-facebook').href = `https://www.facebook.com/sharer/sharer.php?u=${url}`;
        modalEl.querySelector('#share-instagram').href = `https://www.instagram.com/?url=${url}`;
        modalEl.querySelector('#share-telegram').href = `https://t.me/share/url?url=${url}&text=${title}`;
        modalEl.querySelector('#share-x').href = `https://twitter.com/intent/tweet?url=${url}&text=${title}`;
        new bootstrap.Modal(modalEl).show();
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
