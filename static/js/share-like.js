document.addEventListener('DOMContentLoaded', () => {
  function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
      const cookies = document.cookie.split(';');
      for (let i = 0; i < cookies.length; i++) {
        const cookie = cookies[i].trim();
        if (cookie.substring(0, name.length + 1) === (name + '=')) {
          cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
          break;
        }
      }
    }
    return cookieValue;
  }

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
    toast.dataset.bsDelay = '4000';
    toast.innerHTML = `<div class="d-flex"><div class="toast-body">${message}</div><button type="button" class="btn-close btn-close-white me-2 m-auto" data-bs-dismiss="toast" aria-label="Close"></button></div>`;
    container.appendChild(toast);
    new bootstrap.Toast(toast).show();
  }

  const heart = document.getElementById('club-heart');
  if (heart) {
    heart.addEventListener('click', async () => {
      const url = heart.dataset.url;
      const csrf = getCookie('csrftoken');
      try {
        const res = await fetch(url, {
          method: 'POST',
          headers: { 'X-CSRFToken': csrf }
        });
        if (res.ok) {
          heart.classList.toggle('liked');
          const followed = heart.classList.contains('liked');
          showToast(followed ? 'Ahora sigues al club' : 'Has dejado de seguir al club');
        }
      } catch (err) {
        console.error(err);
      }
    });
  }

  const shareBtn = document.getElementById('club-share');
  if (shareBtn) {
    shareBtn.addEventListener('click', async () => {
      const url = window.location.href;
      if (navigator.share) {
        try {
          await navigator.share({ url });
        } catch (err) {
          console.error(err);
        }
      } else if (navigator.clipboard) {
        try {
          await navigator.clipboard.writeText(url);
          alert('Enlace copiado al portapapeles');
        } catch (err) {
          prompt('Copia este enlace:', url);
        }
      } else {
        prompt('Copia este enlace:', url);
      }
    });
  }
});