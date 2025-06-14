document.addEventListener('DOMContentLoaded', () => {
  const heart = document.getElementById('club-heart');
  if (heart) {
    heart.addEventListener('click', async () => {
      const url = heart.dataset.url;
      const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;
      try {
        const res = await fetch(url, {
          method: 'POST',
          headers: { 'X-CSRFToken': csrftoken },
          credentials: 'same-origin'
        });
        if (res.redirected) {
          const modal = new bootstrap.Modal(document.getElementById('loginModal'));
          modal.show();
          return;
        }
        if (res.ok) {
          const data = await res.json();
          heart.classList.toggle('liked', data.following);
          if (data.message) {
            showToast(data.message);
          }
        }
      } catch (err) {
        console.error(err);
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
