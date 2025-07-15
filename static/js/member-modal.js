document.addEventListener('DOMContentLoaded', () => {
  const profileEl = document.getElementById('memberProfileModal');
  const editEl = document.getElementById('editMemberModal');
  const profileModal = profileEl ? new bootstrap.Modal(profileEl) : null;
  const editModal = editEl ? new bootstrap.Modal(editEl) : null;

  document.querySelectorAll('.view-member-btn').forEach(btn => {
    btn.addEventListener('click', () => {
      const id = btn.dataset.memberId;
      fetch(`/clubs/miembro/${id}/detalle/`)
        .then(res => res.text())
        .then(html => {
          if (profileEl) {
            profileEl.querySelector('.modal-body').innerHTML = html;
            profileModal.show();
          }
        });
    });
  });

  document.querySelectorAll('.edit-member-btn').forEach(btn => {
    btn.addEventListener('click', () => {
      const id = btn.dataset.memberId;
      fetch(`/clubs/miembro/${id}/editar/`, { headers: { 'X-Requested-With': 'XMLHttpRequest' } })
        .then(res => res.text())
        .then(html => {
          if (editEl) {
            editEl.querySelector('.modal-body').innerHTML = html;
            const form = editEl.querySelector('form');
            form.addEventListener('submit', e => {
              e.preventDefault();
              const fd = new FormData(form);
              fetch(form.action, { method: 'POST', headers: { 'X-Requested-With': 'XMLHttpRequest' }, body: fd })
                .then(() => window.location.reload());
            });
            editModal.show();
          }
        });
    });
  });
});
