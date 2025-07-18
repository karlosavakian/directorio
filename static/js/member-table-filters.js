document.addEventListener('DOMContentLoaded', () => {
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

  const estadoToggle = document.getElementById('estado-filter-btn');
  const pagoToggle = document.getElementById('pago-filter-btn');

  const closeDropdown = (toggle) => {
    if (window.bootstrap && toggle) {
      const instance = bootstrap.Dropdown.getInstance(toggle);
      if (instance) instance.hide();
    }
  };

  document.getElementById('apply-estado-filter')?.addEventListener('click', () => {
    const radio = document.querySelector('#estado-filter-menu input[name="estado-filter"]:checked');
    selectedEstado = radio ? radio.value : '';
    filterRows();
    closeDropdown(estadoToggle);
  });

  document.getElementById('cancel-estado-filter')?.addEventListener('click', () => {
    const current = document.querySelector(`#estado-filter-menu input[name="estado-filter"][value="${selectedEstado}"]`);
    if (current) current.checked = true;
    closeDropdown(estadoToggle);
  });

  document.getElementById('apply-pago-filter')?.addEventListener('click', () => {
    const radio = document.querySelector('#pago-filter-menu input[name="pago-filter"]:checked');
    selectedPago = radio ? radio.value : '';
    filterRows();
    closeDropdown(pagoToggle);
  });

  document.getElementById('cancel-pago-filter')?.addEventListener('click', () => {
    const current = document.querySelector(`#pago-filter-menu input[name="pago-filter"][value="${selectedPago}"]`);
    if (current) current.checked = true;
    closeDropdown(pagoToggle);
  });
});
