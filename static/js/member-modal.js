document.addEventListener('DOMContentLoaded', () => {
  const profileEl = document.getElementById('memberProfileModal');
  const editEl = document.getElementById('editMemberModal');
  const addEl = document.getElementById('addMemberModal');
  const confirmEl = document.getElementById('confirmEditModal');
  const profileModal = profileEl ? new bootstrap.Modal(profileEl) : null;
  const editModal = editEl ? new bootstrap.Modal(editEl) : null;
  const addModal = addEl ? new bootstrap.Modal(addEl) : null;
  const confirmModal = confirmEl ? new bootstrap.Modal(confirmEl) : null;
  let formToSubmit = null;

  if (confirmEl) {
    confirmEl.querySelector('.confirm-edit').addEventListener('click', () => {
      if (!formToSubmit) return;
      const fd = new FormData(formToSubmit);
      fetch(formToSubmit.action, {
        method: 'POST',
        headers: { 'X-Requested-With': 'XMLHttpRequest' },
        body: fd
      }).then(() => window.location.reload());
    });
  }

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
            if (window.initSelectLabels) {
              window.initSelectLabels(editEl);
            }
            const form = editEl.querySelector('form');
            form.addEventListener('submit', e => {
              e.preventDefault();
              formToSubmit = form;
              if (confirmModal) {
                confirmModal.show();
              } else {
                const fd = new FormData(form);
                fetch(form.action, { method: 'POST', headers: { 'X-Requested-With': 'XMLHttpRequest' }, body: fd })
                  .then(() => window.location.reload());
              }
            });
            editModal.show();
          }
        });
    });
  });

  const addBtn = document.querySelector('.add-member-btn');
  if (addBtn) {
    addBtn.addEventListener('click', () => {
      const slug = addBtn.dataset.clubSlug;
      fetch(`/clubs/${slug}/miembro/nuevo/`, { headers: { 'X-Requested-With': 'XMLHttpRequest' } })
        .then(res => res.text())
        .then(html => {
          if (addEl) {
            addEl.querySelector('.modal-body').innerHTML = html;
            if (window.initAvatarDropzones) {
              window.initAvatarDropzones(addEl);
            }
            if (window.initSelectLabels) {
              window.initSelectLabels(addEl);
            }
            const form = addEl.querySelector('form');
            form.addEventListener('submit', e => {
              e.preventDefault();
              const fd = new FormData(form);
              fetch(form.action, { method: 'POST', headers: { 'X-Requested-With': 'XMLHttpRequest' }, body: fd })
                .then(() => window.location.reload());
            });
            addModal.show();
          }
        });
    });
  }
});
