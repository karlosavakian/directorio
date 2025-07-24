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
            form.addEventListener('submit', e => {
              e.preventDefault();
              const fd = new FormData(form);
              fetch(form.action || `/clubs/${slug}/clase/nueva/`, {
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
