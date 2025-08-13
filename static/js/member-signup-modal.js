document.addEventListener('DOMContentLoaded', () => {
  const modalEl = document.getElementById('memberSignupModal');
  const modal = modalEl ? new bootstrap.Modal(modalEl) : null;
  const btn = document.querySelector('.signup-member-btn');
  if (btn) {
    btn.addEventListener('click', () => {
      const slug = btn.dataset.clubSlug;
        fetch(`/@${slug}/inscribirse/`, { headers: { "X-Requested-With": "XMLHttpRequest" } })
        .then(res => res.text())
        .then(html => {
          if (modalEl) {
            modalEl.querySelector('.modal-body').innerHTML = html;
            if (window.initAvatarDropzones) {
              window.initAvatarDropzones(modalEl);
            }
            if (window.initSelectLabels) {
              window.initSelectLabels(modalEl);
            }
            if (window.initPhoneInputs) {
              window.initPhoneInputs(modalEl);
            }
            if (window.initMemberLocationSelects) {
              window.initMemberLocationSelects(modalEl);
            }
            const form = modalEl.querySelector('form');
            form.addEventListener('submit', e => {
              e.preventDefault();
              if (!confirm('¿Confirmas tu inscripción?')) return;
              const fd = new FormData(form);
              fetch(form.action, { method: 'POST', headers: { 'X-Requested-With': 'XMLHttpRequest' }, body: fd })
                .then(res => {
                  if (res.status === 204) {
                    showToast('Inscripción completada con éxito');
                    modal.hide();
                  } else {
                    return res.text().then(html => {
                      modalEl.querySelector('.modal-body').innerHTML = html;
                    });
                  }
                });
            });
            modal.show();
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
