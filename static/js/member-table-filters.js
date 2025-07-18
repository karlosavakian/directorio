document.addEventListener('DOMContentLoaded', () => {
  const estadoForm = document.getElementById('estado-filter-menu');
  const pagoForm = document.getElementById('pago-filter-menu');
  const estadoBtn = document.getElementById('estado-filter-btn');
  const pagoBtn = document.getElementById('pago-filter-btn');
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

  function restoreRadio(form, value) {
    const radios = form.querySelectorAll('input[type="radio"]');
    radios.forEach(r => {
      r.checked = r.value === value;
    });
  }

  if (estadoForm) {
    const dd = bootstrap.Dropdown.getOrCreateInstance(estadoBtn);
    estadoBtn.addEventListener('click', () => restoreRadio(estadoForm, selectedEstado));
    estadoForm.addEventListener('submit', e => {
      e.preventDefault();
      const checked = estadoForm.querySelector('input[name="estado-filter"]:checked');
      selectedEstado = checked ? checked.value : '';
      dd.hide();
      filterRows();
    });
    const cancel = estadoForm.querySelector('.cancel-filter');
    if (cancel) {
      cancel.addEventListener('click', () => {
        estadoForm.querySelectorAll('input[type="radio"]').forEach(r => {
          r.checked = false;
        });
        selectedEstado = '';
        dd.hide();
        filterRows();
      });
    }
  }

  if (pagoForm) {
    const dd = bootstrap.Dropdown.getOrCreateInstance(pagoBtn);
    pagoBtn.addEventListener('click', () => restoreRadio(pagoForm, selectedPago));
    pagoForm.addEventListener('submit', e => {
      e.preventDefault();
      const checked = pagoForm.querySelector('input[name="pago-filter"]:checked');
      selectedPago = checked ? checked.value : '';
      dd.hide();
      filterRows();
    });
    const cancel = pagoForm.querySelector('.cancel-filter');
    if (cancel) {
      cancel.addEventListener('click', () => {
        pagoForm.querySelectorAll('input[type="radio"]').forEach(r => {
          r.checked = false;
        });
        selectedPago = '';
        dd.hide();
        filterRows();
      });
    }
  }
});
