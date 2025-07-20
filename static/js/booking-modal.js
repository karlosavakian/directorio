document.addEventListener('DOMContentLoaded', () => {
  const modalEl = document.getElementById('bookingModal');
  const modal = modalEl ? new bootstrap.Modal(modalEl) : null;
  const btn = document.querySelector('.booking-btn');
  if (btn && modal) {
    btn.addEventListener('click', () => {
      modal.show();
    });
    const form = modalEl.querySelector('#booking-form');
    form.addEventListener('submit', e => {
      e.preventDefault();
      modal.hide();
    });
  }
});
