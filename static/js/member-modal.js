document.addEventListener('DOMContentLoaded', () => {
  const profileEl = document.getElementById('memberProfileModal');
  const editEl = document.getElementById('editMemberModal');
  const addEl = document.getElementById('addMemberModal');
  const profileModal = profileEl ? new bootstrap.Modal(profileEl) : null;
  const editModal = editEl ? new bootstrap.Modal(editEl) : null;
  const addModal = addEl ? new bootstrap.Modal(addEl) : null;

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
            if (window.initAvatarDropzones) {
              window.initAvatarDropzones(editEl);
            }
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
