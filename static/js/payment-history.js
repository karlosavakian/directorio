document.addEventListener('DOMContentLoaded', () => {
  const modalEl = document.getElementById('paymentHistoryModal');
  if (!modalEl) return;
  const modal = new bootstrap.Modal(modalEl);
  modalEl.querySelector('.modal-body').innerHTML = '';

  function loadHistory(memberId) {
    fetch(`/clubs/miembro/${memberId}/pagos/`)
      .then(res => res.text())
      .then(html => {
        modalEl.querySelector('.modal-body').innerHTML = html;
        initForm(memberId);
      });
  }

  function initForm(memberId) {
    const toggleBtn = modalEl.querySelector('#add-payment-btn');
    const form = modalEl.querySelector('#payment-form');
    if (!toggleBtn || !form) return;
    toggleBtn.addEventListener('click', () => {
      form.classList.toggle('d-none');
    });
    form.addEventListener('submit', e => {
      e.preventDefault();
      const formData = new FormData(form);
      fetch(form.action, {
        method: 'POST',
        headers: { 'X-Requested-With': 'XMLHttpRequest' },
        body: formData
      }).then(() => loadHistory(memberId));
    });
  }

  document.querySelectorAll('.view-payments-btn').forEach(btn => {
    btn.addEventListener('click', () => {
      const memberId = btn.dataset.memberId;
      loadHistory(memberId);
      modal.show();
    });
  });
});
