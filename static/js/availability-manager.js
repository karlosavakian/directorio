document.addEventListener('DOMContentLoaded', () => {
  const table = document.getElementById('availability-table');
  if (!table) return;
  const manager = document.getElementById('availability-manager');
  const clubSlug = manager?.dataset.clubSlug || 'default';
  const monthSelect = document.getElementById('availability-month');
  const yearSelect = document.getElementById('availability-year');
  const prevBtn = document.getElementById('availability-prev');
  const nextBtn = document.getElementById('availability-next');
  const clearBtn = document.getElementById('availability-clear');


  let availability = {};
  try {
    availability = JSON.parse(localStorage.getItem('availability-' + clubSlug)) || {};
  } catch {
    availability = {};
  }
  let hours = [];
  let hoursMap = {};

  const DAYS_STEP = 10;
  const today = new Date();
  let startDate = new Date(today.getFullYear(), today.getMonth(), today.getDate());
  const endOfYear = new Date(today.getFullYear(), 11, 31);

  document.addEventListener('scheduleHoursUpdate', e => {
    if (e.detail?.hours) {
      hours = e.detail.hours;
    }
    if (e.detail?.hoursMap) {
      hoursMap = e.detail.hoursMap;
      if (!hours.length) {
        hours = Array.from(
          new Set(Object.values(hoursMap).reduce((a, v) => a.concat(v || []), []))
        ).sort();
      }
    }
    buildTable();
    saveAvailability();
  });

  function updateSelectors() {
    monthSelect.value = startDate.getMonth();
    yearSelect.value = startDate.getFullYear();
  }

  function updateCellColor(td, value) {
    td.classList.toggle('bg-danger', value === 0);
    td.classList.toggle('bg-warning', value === 1);
    td.classList.toggle('bg-success', value >= 2);
  }

  function buildTable() {
    updateSelectors();
    const dayNames = ['Dom', 'Lun', 'Mar', 'Mié', 'Jue', 'Vie', 'Sáb'];
    const maxDays = Math.min(
      DAYS_STEP,
      Math.floor((endOfYear - startDate) / (24 * 60 * 60 * 1000)) + 1
    );

    const thead = table.querySelector('thead');
    thead.innerHTML = '';
    const headRow = document.createElement('tr');
    const empty = document.createElement('th');
    headRow.appendChild(empty);
    for (let i = 0; i < maxDays; i++) {
      const date = new Date(startDate);
      date.setDate(startDate.getDate() + i);
      const dow = dayNames[date.getDay()];
      const th = document.createElement('th');
      const dayDiv = document.createElement('div');
      dayDiv.className = 'small';
      dayDiv.textContent = dow;
      const numDiv = document.createElement('div');
      numDiv.textContent = date.getDate();
      th.appendChild(dayDiv);
      th.appendChild(numDiv);
      headRow.appendChild(th);
    }
    thead.appendChild(headRow);

    // Row with add-time pickers
    const addRow = document.createElement('tr');
    const addEmpty = document.createElement('th');
    addRow.appendChild(addEmpty);
    for (let i = 0; i < maxDays; i++) {
      const date = new Date(startDate);
      date.setDate(startDate.getDate() + i);
      const dateStr = date.toISOString().split('T')[0];
      const th = document.createElement('th');
      const form = document.createElement('form');
      form.className = 'd-flex gap-1';
      const input = document.createElement('input');
      input.type = 'time';
      input.required = true;
      input.className = 'form-control form-control-sm';
      const btn = document.createElement('button');
      btn.type = 'submit';
      btn.className = 'btn btn-sm btn-dark';
      btn.innerHTML = '<i class="bi bi-plus-circle"></i>';
      form.appendChild(input);
      form.appendChild(btn);
      form.addEventListener('submit', e => {
        e.preventDefault();
        const val = input.value;
        if (!val) return;
        addTime(dateStr, val);
        input.value = '';
      });
      th.appendChild(form);
      addRow.appendChild(th);
    }
    thead.appendChild(addRow);

    const tbody = table.querySelector('tbody');
    tbody.innerHTML = '';
    // When no hours are defined by the schedule manager we
    // shouldn't populate the table with the full 24 hour range.
    // Instead leave it empty so hours are only those introduced
    // by the manager.
    const timeList = hours.length ? hours.slice().sort() : [];
    for (const t of timeList) {
      const row = document.createElement('tr');
      const th = document.createElement('th');
      const label = document.createElement('span');
      label.textContent = t;
      const delBtn = document.createElement('button');
      delBtn.type = 'button';
      delBtn.className = 'btn btn-link btn-sm text-danger ms-1';
      delBtn.innerHTML = '<i class="bi bi-dash-circle"></i>';
      delBtn.addEventListener('click', () => removeTime(t));
      th.appendChild(label);
      th.appendChild(delBtn);
      row.appendChild(th);
      for (let i = 0; i < maxDays; i++) {
        const date = new Date(startDate);
        date.setDate(startDate.getDate() + i);
        const dateStr = date.toISOString().split('T')[0];
        const timeStr = t;
        const td = document.createElement('td');
        const input = document.createElement('input');
        input.type = 'number';
        input.min = '0';
        input.dataset.date = dateStr;
        input.dataset.time = timeStr;
        let val = availability[dateStr]?.[timeStr];
        if (val === undefined) {
          val = hoursMap[dateStr]?.includes(timeStr) ? 1 : 0;
        }
        input.value = val;
        input.className = 'form-control form-control-sm text-center';
        input.addEventListener('input', () => {
          const v = parseInt(input.value, 10) || 0;
          updateCellColor(td, v);
        });
        updateCellColor(td, val);
        td.appendChild(input);
        row.appendChild(td);
      }
      tbody.appendChild(row);
    }
    document.dispatchEvent(
      new CustomEvent('availabilityDateChange', {
        detail: { startDate: startDate.toISOString() },
      })
    );
  }

  function saveAvailability() {
    table.querySelectorAll('tbody input').forEach(input => {
      const date = input.dataset.date;
      const time = input.dataset.time;
      const val = parseInt(input.value, 10) || 0;
      if (!availability[date]) availability[date] = {};
      availability[date][time] = val;
    });
    localStorage.setItem('availability-' + clubSlug, JSON.stringify(availability));
  }

  function addTime(dateStr, timeStr) {
    if (!hours.includes(timeStr)) hours.push(timeStr);
    if (!hoursMap[dateStr]) hoursMap[dateStr] = [];
    if (!hoursMap[dateStr].includes(timeStr)) hoursMap[dateStr].push(timeStr);
    buildTable();
    saveAvailability();
  }

  function removeTime(timeStr) {
    hours = hours.filter(t => t !== timeStr);
    for (const d in hoursMap) {
      hoursMap[d] = (hoursMap[d] || []).filter(t => t !== timeStr);
    }
    for (const d in availability) {
      if (availability[d]) {
        delete availability[d][timeStr];
        if (Object.keys(availability[d]).length === 0) delete availability[d];
      }
    }
    buildTable();
    saveAvailability();
  }

  function changeDays(step) {
    const newDate = new Date(startDate);
    newDate.setDate(newDate.getDate() + step * DAYS_STEP);
    if (newDate < today) {
      startDate = new Date(today);
    } else if (newDate > endOfYear) {
      startDate = new Date(endOfYear);
      startDate.setDate(endOfYear.getDate() - DAYS_STEP + 1);
      if (startDate < today) startDate = new Date(today);
    } else {
      startDate = newDate;
    }
    buildTable();
  }

  monthSelect.addEventListener('change', () => {
    const month = parseInt(monthSelect.value, 10);
    const year = parseInt(yearSelect.value, 10);
    startDate = new Date(year, month, 1);
    if (startDate < today) startDate = new Date(today);
    buildTable();
  });

  yearSelect.addEventListener('change', () => {
    const month = parseInt(monthSelect.value, 10);
    const year = parseInt(yearSelect.value, 10);
    startDate = new Date(year, month, 1);
    if (startDate < today) startDate = new Date(today);
    buildTable();
  });

  if (prevBtn) prevBtn.addEventListener('click', () => changeDays(-1));
  if (nextBtn) nextBtn.addEventListener('click', () => changeDays(1));
  buildTable();
  saveAvailability();

  const saveBtn = document.getElementById('availability-save');
  if (saveBtn) {
    saveBtn.addEventListener('click', () => {
      saveAvailability();
      alert('Cambios guardados');
    });
  }

  if (clearBtn) {
    clearBtn.addEventListener('click', () => {
      availability = {};
      table.querySelectorAll('tbody input').forEach(input => {
        input.value = 0;
        updateCellColor(input.closest('td'), 0);
      });
      localStorage.removeItem('availability-' + clubSlug);
    });
  }
});

