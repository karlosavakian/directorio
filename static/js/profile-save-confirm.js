document.addEventListener('DOMContentLoaded', () => {
  const modalEl = document.getElementById('confirmProfileModal');
  const form = document.querySelector('.profile-form');
  if (!modalEl || !form) return;
  const modal = new bootstrap.Modal(modalEl);
  let confirmed = false;

  form.addEventListener('submit', e => {
    if (confirmed) return;
    e.preventDefault();
    modal.show();
  });

  modalEl.querySelector('.confirm-save').addEventListener('click', () => {
    confirmed = true;
    form.submit();
  });
});

