document.addEventListener('DOMContentLoaded', () => {
  const addEl = document.getElementById('addBookingClassModal');
  const addModal = addEl ? new bootstrap.Modal(addEl) : null;
  const btn = document.querySelector('.add-booking-class-btn');
  if (btn) {
    btn.addEventListener('click', () => {
      const slug = btn.dataset.clubSlug;
      fetch(`/clubs/${slug}/clase/nueva/`, { headers: { 'X-Requested-With': 'XMLHttpRequest' } })
        .then(res => res.text())
        .then(html => {
          if (addEl) {
            addEl.querySelector('.modal-body').innerHTML = html;
            if (window.initSelectLabels) {
              window.initSelectLabels(addEl);
            }
            addEl.querySelectorAll('[data-bs-toggle="tooltip"]').forEach(el => new bootstrap.Tooltip(el));
            const form = addEl.querySelector('form');
            const cancelBtn = form.querySelector('[data-bs-dismiss="modal"]');
            if (cancelBtn) {
              cancelBtn.addEventListener('click', e => {
                e.preventDefault();
                if (confirm('¿Seguro que deseas cancelar?')) {
                  addModal.hide();
                }
              });
            }
            form.addEventListener('submit', e => {
              e.preventDefault();
              const fd = new FormData(form);
              fetch(form.action || `/clubs/${slug}/clase/nueva/`, {
                method: 'POST',
                headers: { 'X-Requested-With': 'XMLHttpRequest' },
                body: fd
              }).then(res => {
                if (res.ok) {
                  showToast('Clase añadida correctamente');
                }
                setTimeout(() => window.location.reload(), 500);
              });
            });
            addModal.show();
          }
        });
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
