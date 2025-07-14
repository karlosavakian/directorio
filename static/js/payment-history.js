document.addEventListener('DOMContentLoaded', () => {
  const modalEl = document.getElementById('paymentHistoryModal');
  if (!modalEl) return;
  const modal = new bootstrap.Modal(modalEl);
  modalEl.querySelector('.modal-body').innerHTML = '';

  document.querySelectorAll('.view-payments-btn').forEach(btn => {
    btn.addEventListener('click', () => {
      const memberId = btn.dataset.memberId;
      fetch(`/clubs/miembro/${memberId}/pagos/`)
        .then(res => res.text())
        .then(html => {
          modalEl.querySelector('.modal-body').innerHTML = html;
          modal.show();
        });
    });
  });
});
