document.addEventListener('DOMContentLoaded', () => {
  document.querySelectorAll('[data-bs-toggle="tooltip"]').forEach(el => {
    new bootstrap.Tooltip(el);
  });
  const addEl = document.getElementById('addBookingClassModal');
  const editEl = document.getElementById('editBookingClassModal');
  const addModal = addEl ? new bootstrap.Modal(addEl) : null;
  const editModal = editEl ? new bootstrap.Modal(editEl) : null;

  const addBtn = document.querySelector('.add-booking-class-btn');
  if (addBtn) {
    addBtn.addEventListener('click', () => {
      const slug = addBtn.dataset.clubSlug;
      fetch(`/clubs/${slug}/clase/nueva/`, {
        headers: { 'X-Requested-With': 'XMLHttpRequest' }
      })
        .then(res => res.text())
        .then(html => {
          if (addEl) {
            addEl.querySelector('.modal-body').innerHTML = html;
            if (window.initSelectLabels) {
              window.initSelectLabels(addEl);
            }
            const form = addEl.querySelector('form');
            if (form) {
              form.addEventListener('submit', e => {
                e.preventDefault();
                const fd = new FormData(form);
                fetch(form.action, {
                  method: 'POST',
                  headers: { 'X-Requested-With': 'XMLHttpRequest' },
                  body: fd
                }).then(() => window.location.reload());
              });
            }
            addModal && addModal.show();
          }
        });
    });
  }

  function bindEditButtons() {
    document.querySelectorAll('.edit-booking-class-btn').forEach(btn => {
      btn.addEventListener('click', () => {
        const id = btn.dataset.classId;
        fetch(`/clubs/clase/${id}/editar/`, {
          headers: { 'X-Requested-With': 'XMLHttpRequest' }
        })
          .then(res => res.text())
          .then(html => {
            if (editEl) {
              editEl.querySelector('.modal-body').innerHTML = html;
              if (window.initSelectLabels) {
                window.initSelectLabels(editEl);
              }
              const form = editEl.querySelector('form');
              if (form) {
                form.addEventListener('submit', e => {
                  e.preventDefault();
                  const fd = new FormData(form);
                  fetch(form.action, {
                    method: 'POST',
                    headers: { 'X-Requested-With': 'XMLHttpRequest' },
                    body: fd
                  }).then(() => window.location.reload());
                });
              }
              editModal && editModal.show();
            }
          });
      });
    });
  }

  bindEditButtons();
});
