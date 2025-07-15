document.addEventListener('DOMContentLoaded', () => {
  const addEl = document.getElementById('addCoachModal');
  const addModal = addEl ? new bootstrap.Modal(addEl) : null;
  const btn = document.querySelector('.add-coach-btn');
  if (btn) {
    btn.addEventListener('click', () => {
      const slug = btn.dataset.clubSlug;
      fetch(`/clubs/${slug}/entrenador/nuevo/`, {
        headers: { 'X-Requested-With': 'XMLHttpRequest' }
      })
        .then(res => res.text())
        .then(html => {
          if (addEl) {
            addEl.querySelector('.modal-body').innerHTML = html;
            if (window.initAvatarDropzones) {
              window.initAvatarDropzones(addEl);
            }
            const form = addEl.querySelector('form');
            form.addEventListener('submit', e => {
              e.preventDefault();
              const fd = new FormData(form);
              fetch(form.action, {
                method: 'POST',
                headers: { 'X-Requested-With': 'XMLHttpRequest' },
                body: fd
              }).then(() => window.location.reload());
            });
            addModal.show();
          }
        });
    });
  }
});
