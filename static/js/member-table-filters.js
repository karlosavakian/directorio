document.addEventListener('DOMContentLoaded', () => {
  const estadoItems = document.querySelectorAll('#estado-filter-menu .estado-option');
  const pagoItems = document.querySelectorAll('#pago-filter-menu .pago-option');
  const rows = document.querySelectorAll('#tab-members tbody tr');
  const emptyRow = document.querySelector('#tab-members tbody .no-members-row');

  let selectedEstado = '';
  let selectedPago = '';

  function filterRows() {
    let shown = 0;
    rows.forEach(row => {
      if (row.classList.contains('no-members-row')) return;
      const est = row.getAttribute('data-estado');
      const pag = row.getAttribute('data-pago');
      const matchEstado = !selectedEstado || est === selectedEstado;
      const matchPago = !selectedPago || pag === selectedPago;
      if (matchEstado && matchPago) {
        row.style.display = '';
        shown++;
      } else {
        row.style.display = 'none';
      }
    });
    if (emptyRow) {
      emptyRow.style.display = shown ? 'none' : '';
    }
  }

  estadoItems.forEach(item => {
    item.addEventListener('click', () => {
      selectedEstado = item.dataset.value || '';
      estadoItems.forEach(i => i.classList.remove('active'));
      item.classList.add('active');
      filterRows();
    });
  });

  pagoItems.forEach(item => {
    item.addEventListener('click', () => {
      selectedPago = item.dataset.value || '';
      pagoItems.forEach(i => i.classList.remove('active'));
      item.classList.add('active');
      filterRows();
    });
  });
});
