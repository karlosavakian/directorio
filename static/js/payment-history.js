document.addEventListener('DOMContentLoaded', () => {
  const modalEl = document.getElementById('paymentHistoryModal');
  if (!modalEl) return;
  const modal = new bootstrap.Modal(modalEl);
  modalEl.querySelector('.modal-body').innerHTML = '';
  let createAction = '';

  function loadHistory(memberId) {
    fetch(`/clubs/miembro/${memberId}/pagos/`)
      .then(res => res.text())
      .then(html => {
        modalEl.querySelector('.modal-body').innerHTML = html;
        initForm(memberId);
        initEdit(memberId);
        initDelete(memberId);
      });
  }

  function initForm(memberId) {
    const toggleBtn = modalEl.querySelector('#add-payment-btn');
    const form = modalEl.querySelector('#payment-form');
    if (!toggleBtn || !form) return;
    createAction = form.action;
    toggleBtn.addEventListener('click', () => {
      form.classList.toggle('d-none');
      form.action = createAction;
      form.reset();
      const cancelBtn = form.querySelector('.cancel-edit');
      if (cancelBtn) cancelBtn.remove();
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

  function initEdit(memberId) {
    const form = modalEl.querySelector('#payment-form');
    if (!form) return;
    modalEl.querySelectorAll('.edit-payment-btn').forEach(btn => {
      btn.addEventListener('click', () => {
        form.classList.remove('d-none');
        form.action = btn.dataset.url;
        form.querySelector('input[name="fecha"]').value = btn.dataset.fecha;
        form.querySelector('input[name="monto"]').value = btn.dataset.monto;
        if (!form.querySelector('.cancel-edit')) {
          const cancel = document.createElement('button');
          cancel.type = 'button';
          cancel.textContent = 'Cancelar';
          cancel.className = 'btn btn-secondary btn-sm ms-2 cancel-edit';
          form.querySelector('.col-auto').appendChild(cancel);
          cancel.addEventListener('click', () => {
            form.action = createAction;
            form.reset();
            cancel.remove();
          });
        }
      });
    });
  }

  function initDelete(memberId) {
    modalEl.querySelectorAll('.delete-payment-form').forEach(form => {
      form.addEventListener('submit', e => {
        e.preventDefault();
        const alert = document.createElement('div');
        alert.className = 'alert alert-warning d-flex justify-content-between align-items-center';
        alert.innerHTML = '<span>¿Seguro que deseas eliminar este pago?</span>' +
          '<div><button type="button" class="btn btn-danger btn-sm me-2 confirm">Eliminar</button>' +
          '<button type="button" class="btn btn-secondary btn-sm cancel">Cancelar</button></div>';
        modalEl.querySelector('.modal-body').prepend(alert);
        alert.querySelector('.cancel').addEventListener('click', () => alert.remove());
        alert.querySelector('.confirm').addEventListener('click', () => {
          const formData = new FormData(form);
          fetch(form.action, {
            method: 'POST',
            headers: { 'X-Requested-With': 'XMLHttpRequest' },
            body: formData
          }).then(() => {
            alert.remove();
            loadHistory(memberId);
          });
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
