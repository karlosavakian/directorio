document.addEventListener('DOMContentLoaded', () => {
  const table = document.getElementById('availability-table');
  if (!table) return;
  const monthSelect = document.getElementById('availability-month');
  const yearSelect = document.getElementById('availability-year');
  const prevBtn = document.getElementById('availability-prev');
  const nextBtn = document.getElementById('availability-next');

  function updateCellColor(td, value) {
    td.classList.toggle('bg-danger', value === 0);
    td.classList.toggle('bg-success', value > 0);
  }

  function buildTable() {
    const dayNames = ['Dom', 'Lun', 'Mar', 'Mié', 'Jue', 'Vie', 'Sáb'];
    const month = parseInt(monthSelect.value, 10);
    const year = parseInt(yearSelect.value, 10);
    const daysInMonth = new Date(year, month + 1, 0).getDate();
    const maxDays = Math.min(daysInMonth, 10);

    const thead = table.querySelector('thead');
    thead.innerHTML = '';
    const headRow = document.createElement('tr');
    const empty = document.createElement('th');
    headRow.appendChild(empty);
    for (let d = 1; d <= maxDays; d++) {
      const date = new Date(year, month, d);
      const dow = dayNames[date.getDay()];
      const th = document.createElement('th');
      const dayDiv = document.createElement('div');
      dayDiv.className = 'small';
      dayDiv.textContent = dow;
      const numDiv = document.createElement('div');
      numDiv.textContent = d;
      th.appendChild(dayDiv);
      th.appendChild(numDiv);
      headRow.appendChild(th);
    }
    thead.appendChild(headRow);

    const tbody = table.querySelector('tbody');
    tbody.innerHTML = '';
    for (let h = 0; h < 24; h++) {
      const row = document.createElement('tr');
      const th = document.createElement('th');
      th.textContent = `${String(h).padStart(2, '0')}:00`;
      row.appendChild(th);
      for (let d = 1; d <= maxDays; d++) {
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

  function changeMonth(offset) {
    let month = parseInt(monthSelect.value, 10);
    let year = parseInt(yearSelect.value, 10);
    month += offset;
    if (month < 0) {
      month = 11;
      year -= 1;
    } else if (month > 11) {
      month = 0;
      year += 1;
    }
    monthSelect.value = month;
    let yearOption = Array.from(yearSelect.options).find((o) => parseInt(o.value, 10) === year);
    if (!yearOption) {
      yearOption = document.createElement('option');
      yearOption.value = year;
      yearOption.textContent = year;
      yearSelect.appendChild(yearOption);
    }
    yearSelect.value = year;
    buildTable();
  }

  monthSelect.addEventListener('change', buildTable);
  yearSelect.addEventListener('change', buildTable);
  if (prevBtn) prevBtn.addEventListener('click', () => changeMonth(-1));
  if (nextBtn) nextBtn.addEventListener('click', () => changeMonth(1));
  buildTable();

  const saveBtn = document.getElementById('availability-save');
  if (saveBtn) {
    saveBtn.addEventListener('click', () => {
      alert('Cambios guardados (demo).');
    });
  }
});

