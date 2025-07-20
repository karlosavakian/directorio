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
            const form = modalEl.querySelector('form');
            form.addEventListener('submit', e => {
              e.preventDefault();
              const fd = new FormData(form);
              fetch(form.action, { method: 'POST', headers: { 'X-Requested-With': 'XMLHttpRequest' }, body: fd })
                .then(() => {
                  modal.hide();
                });
            });
            modal.show();
          }
        });
    });
  }
});
