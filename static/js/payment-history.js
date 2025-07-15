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
        initCreateForm(memberId);
        initEditButtons(memberId);
        initDeleteForms(memberId);
      });
  }

  function initCreateForm(memberId) {
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

  function initEditButtons(memberId) {
    modalEl.querySelectorAll('.edit-payment-btn').forEach(btn => {
      btn.addEventListener('click', e => {
        e.preventDefault();
        fetch(btn.href, { headers: { 'X-Requested-With': 'XMLHttpRequest' } })
          .then(res => res.text())
          .then(html => {
            modalEl.querySelector('.modal-body').innerHTML = html;
            const form = modalEl.querySelector('#edit-payment-form');
            const cancelBtn = modalEl.querySelector('#cancel-edit');
            form.addEventListener('submit', fe => {
              fe.preventDefault();
              const fd = new FormData(form);
              fetch(form.action, {
                method: 'POST',
                headers: { 'X-Requested-With': 'XMLHttpRequest' },
                body: fd
              }).then(() => loadHistory(memberId));
            });
            cancelBtn.addEventListener('click', () => loadHistory(memberId));
          });
      });
    });
  }

  function showDeleteConfirm(onConfirm) {
    const box = modalEl.querySelector('#delete-confirm-box');
    if (!box) return onConfirm();
    box.classList.remove('d-none');
    const cancelBtn = box.querySelector('.cancel-delete');
    const confirmBtn = box.querySelector('.confirm-delete');
    const cleanup = () => {
      box.classList.add('d-none');
      cancelBtn.removeEventListener('click', cancel);
      confirmBtn.removeEventListener('click', confirm);
    };
    const cancel = () => cleanup();
    const confirm = () => {
      cleanup();
      onConfirm();
    };
    cancelBtn.addEventListener('click', cancel);
    confirmBtn.addEventListener('click', confirm);
  }

  function initDeleteForms(memberId) {
    modalEl.querySelectorAll('.delete-payment-form').forEach(form => {
      form.addEventListener('submit', e => {
        e.preventDefault();
        showDeleteConfirm(() => {
          fetch(form.action, {
            method: 'POST',
            headers: { 'X-Requested-With': 'XMLHttpRequest' },
            body: new FormData(form)
          }).then(() => loadHistory(memberId));
        });
      });
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
