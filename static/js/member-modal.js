document.addEventListener('DOMContentLoaded', () => {
  const profileEl = document.getElementById('memberProfileModal');
  const editEl = document.getElementById('editMemberModal');
  const addEl = document.getElementById('addMemberModal');
  const profileModal = profileEl ? new bootstrap.Modal(profileEl) : null;
  const editModal = editEl ? new bootstrap.Modal(editEl) : null;
  const addModal = addEl ? new bootstrap.Modal(addEl) : null;
  let formToSubmit = null;
  let confirmContainer = null;

  function bindMemberRow(row) {
    const viewBtn = row.querySelector('.view-member-btn');
    if (viewBtn) {
      viewBtn.addEventListener('click', () => {
        const id = viewBtn.dataset.memberId;
        fetch(`/clubs/miembro/${id}/detalle/`)
          .then(res => res.text())
          .then(html => {
            if (profileEl) {
              profileEl.querySelector('.modal-body').innerHTML = html;
              profileModal.show();
            }
          });
      });
    }
    const editBtn = row.querySelector('.edit-member-btn');
    if (editBtn) {
      editBtn.addEventListener('click', () => {
        const id = editBtn.dataset.memberId;
        fetch(`/clubs/miembro/${id}/editar/`, { headers: { 'X-Requested-With': 'XMLHttpRequest' } })
          .then(res => res.text())
          .then(html => {
            if (editEl) {
              editEl.querySelector('.modal-body').innerHTML = html;
              if (window.initSelectLabels) {
                window.initSelectLabels(editEl);
              }
              if (window.initPhoneInputs) {
                window.initPhoneInputs(editEl);
              }
              if (window.initMemberLocationSelects) {
                window.initMemberLocationSelects(editEl);
              }
              const form = editEl.querySelector('form');
              form.addEventListener('submit', e => {
                e.preventDefault();
                formToSubmit = form;
                confirmContainer = form.querySelector('.confirm-edit-container');
                if (confirmContainer) {
                  confirmContainer.classList.remove('d-none');
                } else {
                  const fd = new FormData(form);
                  fetch(form.action, { method: 'POST', headers: { 'X-Requested-With': 'XMLHttpRequest' }, body: fd })
                    .then(() => window.location.reload());
                }
              });

              confirmContainer = form.querySelector('.confirm-edit-container');
              if (confirmContainer) {
                const confirmBtn = confirmContainer.querySelector('.confirm-edit-btn');
                const cancelBtn = confirmContainer.querySelector('.cancel-confirm');
                if (confirmBtn) {
                  confirmBtn.addEventListener('click', () => {
                    if (!formToSubmit) return;
                    const fd = new FormData(formToSubmit);
                    fetch(formToSubmit.action, {
                      method: 'POST',
                      headers: { 'X-Requested-With': 'XMLHttpRequest' },
                      body: fd
                    }).then(() => window.location.reload());
                  });
                }
                if (cancelBtn) {
                  cancelBtn.addEventListener('click', () => {
                    confirmContainer.classList.add('d-none');
                  });
                }
              }
              editModal.show();
            }
          });
      });
    }
    const payBtn = row.querySelector('.view-payments-btn');
    if (payBtn && window.loadHistory) {
      payBtn.addEventListener('click', () => {
        const memberId = payBtn.dataset.memberId;
        window.loadHistory(memberId);
        const modalEl = document.getElementById('paymentHistoryModal');
        if (modalEl) {
          const modal = bootstrap.Modal.getOrCreateInstance(modalEl);
          modal.show();
        }
      });
    }
  }



  document.querySelectorAll('#tab-members tbody tr').forEach(tr => bindMemberRow(tr));

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
            if (window.initPhoneInputs) {
              window.initPhoneInputs(addEl);
            }
            if (window.initMemberLocationSelects) {
              window.initMemberLocationSelects(addEl);
            }
            const form = addEl.querySelector('form');
            form.addEventListener('submit', e => {
              e.preventDefault();
              const fd = new FormData(form);
              fetch(form.action, { method: 'POST', headers: { 'X-Requested-With': 'XMLHttpRequest' }, body: fd })
                .then(res => res.text())
                .then(html => {
                  const tbody = document.querySelector('#tab-members tbody');
                  if (tbody) {
                    const tmp = document.createElement('tbody');
                    tmp.innerHTML = html.trim();
                    const newRow = tmp.querySelector('tr');
                    if (newRow) {
                      const emptyRow = tbody.querySelector('.no-members-row');
                      if (emptyRow) emptyRow.remove();
                      tbody.appendChild(newRow);
                      bindMemberRow(newRow);
                    }
                  }
                  addModal.hide();
                });
            });
            addModal.show();
          }
        });
    });
  }
});
