document.addEventListener('DOMContentLoaded', () => {
  const modalEl = document.getElementById('confirmDeleteModal');
  if (!modalEl) return;
  const modal = new bootstrap.Modal(modalEl);
  let formToSubmit = null;

  document.querySelectorAll('.delete-profile-form').forEach(form => {
    form.addEventListener('submit', (e) => {
      e.preventDefault();
      formToSubmit = form;
      modal.show();
    });
  });

  modalEl.querySelector('.confirm-delete').addEventListener('click', () => {
    if (formToSubmit) formToSubmit.submit();
  });
});
