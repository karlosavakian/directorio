document.addEventListener('DOMContentLoaded', () => {
  const modalEl = document.getElementById('confirmDeleteModal');
  if (!modalEl) return;
  const modal = new bootstrap.Modal(modalEl);
  let formToSubmit = null;

  document.body.addEventListener('submit', (e) => {
    const form = e.target.closest('.delete-profile-form');
    if (!form) return;
    e.preventDefault();
    formToSubmit = form;
    modal.show();
  });

  modalEl.querySelector('.confirm-delete').addEventListener('click', () => {
    if (formToSubmit) formToSubmit.submit();
  });
});
