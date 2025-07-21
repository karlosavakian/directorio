document.addEventListener('DOMContentLoaded', () => {
  const table = document.getElementById('availability-table');
  if (!table) return;
  const monthSelect = document.getElementById('availability-month');
  const yearSelect = document.getElementById('availability-year');

  function updateCellColor(td, value) {
    td.classList.toggle('bg-danger', value === 0);
    td.classList.toggle('bg-success', value > 0);
  }

  function buildTable() {
    const month = parseInt(monthSelect.value, 10);
    const year = parseInt(yearSelect.value, 10);
    const daysInMonth = new Date(year, month + 1, 0).getDate();
    const thead = table.querySelector('thead');
    thead.innerHTML = '<tr><th></th>';
    for (let d = 1; d <= daysInMonth; d++) {
      thead.innerHTML += `<th>${d}</th>`;
    }
    thead.innerHTML += '</tr>';

    const tbody = table.querySelector('tbody');
    tbody.innerHTML = '';
    for (let h = 0; h < 24; h++) {
      const row = document.createElement('tr');
      const th = document.createElement('th');
      th.textContent = `${String(h).padStart(2, '0')}:00`;
      row.appendChild(th);
      for (let d = 1; d <= daysInMonth; d++) {
        const td = document.createElement('td');
        const input = document.createElement('input');
        input.type = 'number';
        input.min = '0';
        input.value = '0';
        input.className = 'form-control form-control-sm text-center';
        input.addEventListener('input', () => {
          const val = parseInt(input.value, 10) || 0;
          updateCellColor(td, val);
        });
        td.classList.add('bg-danger');
        td.appendChild(input);
        row.appendChild(td);
      }
      tbody.appendChild(row);
    }
  }

  monthSelect.addEventListener('change', buildTable);
  yearSelect.addEventListener('change', buildTable);
  buildTable();

  const saveBtn = document.getElementById('availability-save');
  if (saveBtn) {
    saveBtn.addEventListener('click', () => {
      alert('Cambios guardados (demo).');
    });
  }
});

