// static/js/schedule-manager.js

document.addEventListener('DOMContentLoaded', () => {
  const table = document.getElementById('schedule-table');
  const dataEl = document.getElementById('schedule-data');
  const monthSelect = document.getElementById('schedule-month');
  const yearSelect = document.getElementById('schedule-year');
  const prevBtn = document.getElementById('schedule-prev');
  const nextBtn = document.getElementById('schedule-next');
  const availMonth = document.getElementById('availability-month');
  const availYear = document.getElementById('availability-year');
  // legacy global form elements (kept for backwards compatibility)
  const hoursForm = document.getElementById('schedule-hours-form');
  const dateInput = document.getElementById('schedule-date');
  const timeInput = document.getElementById('schedule-time');
  const hoursList = document.getElementById('schedule-hours-list');
  const clearBtn = document.getElementById('schedule-hours-clear');

  let schedule = {};
  if (dataEl) {
    try {
      schedule = JSON.parse(dataEl.textContent);
    } catch (e) {
      schedule = {};
    }
  }

  const STORAGE_KEY = 'schedule-hours';

  let hoursMap = {};
  function loadHours() {
    try {
      hoursMap = JSON.parse(localStorage.getItem(STORAGE_KEY)) || {};
    } catch {
      hoursMap = {};
    }
  }
  loadHours();

  const DAYS_STEP = 10;
  const dayNames = ['Dom', 'Lun', 'Mar', 'Mié', 'Jue', 'Vie', 'Sáb'];
  const dayKeys = ['domingo','lunes','martes','miercoles','jueves','viernes','sabado'];
  const today = new Date();
  let startDate = new Date(today.getFullYear(), today.getMonth(), today.getDate());
  const endOfYear = new Date(today.getFullYear(), 11, 31);

  function renderDay(listEl, dateKey) {
    listEl.innerHTML = '';
    const arr = hoursMap[dateKey] || [];
    arr.sort().forEach((t, idx) => {
      const li = document.createElement('li');
      li.className = 'mb-1';

      const row = document.createElement('div');
      row.className = 'd-flex justify-content-between align-items-center';
      const text = document.createElement('span');
      text.textContent = t;
      row.appendChild(text);

      const editBtn = document.createElement('button');
      editBtn.type = 'button';
      editBtn.className = 'btn btn-link btn-sm p-0 me-1';
      editBtn.innerHTML = '<i class="bi bi-pencil-square"></i>';

      const delBtn = document.createElement('button');
      delBtn.type = 'button';
      delBtn.className = 'btn btn-link btn-sm text-danger p-0';
      delBtn.innerHTML = '<i class="bi bi-dash-circle"></i>';

      row.appendChild(editBtn);
      row.appendChild(delBtn);
      li.appendChild(row);

      const form = document.createElement('form');
      form.className = 'd-flex gap-2 mt-1';
      form.style.display = 'none';
      const input = document.createElement('input');
      input.type = 'time';
      input.value = t;
      input.className = 'form-control form-control-sm';
      const saveB = document.createElement('button');
      saveB.type = 'submit';
      saveB.className = 'btn btn-sm btn-dark';
      saveB.textContent = 'Guardar';
      form.appendChild(input);
      form.appendChild(saveB);
      li.appendChild(form);

      editBtn.addEventListener('click', () => {
        form.style.display = form.style.display === 'none' ? 'flex' : 'none';
      });

      form.addEventListener('submit', e => {
        e.preventDefault();
        const val = input.value;
        if (!val) return;
        if (arr.includes(val) && val !== t) {
          form.style.display = 'none';
          return;
        }
        arr[idx] = val;
        hoursMap[dateKey] = arr;
        renderDay(listEl, dateKey);
        saveHours();
      });

      delBtn.addEventListener('click', () => {
        hoursMap[dateKey] = arr.filter(h => h !== t);
        renderDay(listEl, dateKey);
        saveHours();
      });

      listEl.appendChild(li);
    });
  }

  function getUnionHours() {
    return Array.from(
      new Set(Object.values(hoursMap).reduce((acc, v) => acc.concat(v || []), []))
    ).sort();
  }

  function renderHours() {
    if (!hoursList) return;
    hoursList.innerHTML = '';
    getUnionHours().forEach(t => {
      const li = document.createElement('li');
      li.textContent = t;
      li.className = 'small';
      hoursList.appendChild(li);
    });
  }

  function saveHours() {
    localStorage.setItem(STORAGE_KEY, JSON.stringify(hoursMap));
    document.dispatchEvent(
      new CustomEvent('scheduleHoursUpdate', {
        detail: { hours: getUnionHours(), hoursMap },
      })
    );
  }

  function updateSelectors() {
    if (!monthSelect || !yearSelect) return;
    monthSelect.value = startDate.getMonth();
    yearSelect.value = startDate.getFullYear();
    if (dateInput) {
      const y = startDate.getFullYear();
      const m = startDate.getMonth();
      const first = `${y}-${String(m + 1).padStart(2, '0')}-01`;
      const lastDay = new Date(y, m + 1, 0).getDate();
      const last = `${y}-${String(m + 1).padStart(2, '0')}-${String(lastDay).padStart(2, '0')}`;
      dateInput.min = first;
      dateInput.max = last;
      if (!dateInput.value) dateInput.value = first;
    }
  }

  function buildTable() {
    if (!table) return;
    updateSelectors();
    const maxDays = Math.min(
      DAYS_STEP,
      Math.floor((endOfYear - startDate) / (24 * 60 * 60 * 1000)) + 1
    );

    const thead = table.querySelector('thead');
    thead.innerHTML = '';
    const headRow = document.createElement('tr');
    for (let i = 0; i < maxDays; i++) {
      const date = new Date(startDate);
      date.setDate(startDate.getDate() + i);
      const th = document.createElement('th');
      const dayDiv = document.createElement('div');
      dayDiv.className = 'small';
      dayDiv.textContent = dayNames[date.getDay()];
      const numDiv = document.createElement('div');
      numDiv.textContent = date.getDate();
      th.appendChild(dayDiv);
      th.appendChild(numDiv);
      headRow.appendChild(th);
    }
    thead.appendChild(headRow);

    const tbody = table.querySelector('tbody');
    tbody.innerHTML = '';
    const row = document.createElement('tr');
    for (let i = 0; i < maxDays; i++) {
      const date = new Date(startDate);
      date.setDate(startDate.getDate() + i);
      const dateKey = date.toISOString().split('T')[0];
      if (!hoursMap[dateKey]) {
        const dowKey = dayKeys[date.getDay()];
        hoursMap[dateKey] = (schedule[dowKey] || []).map(b => b.hora_inicio);
      }
      const cell = document.createElement('td');
      cell.style.verticalAlign = 'top';

      const btn = document.createElement('button');
      btn.type = 'button';
      btn.className = 'btn btn-outline-dark btn-sm w-100';
      btn.dataset.bsToggle = 'collapse';
      btn.dataset.bsTarget = `#hours-add-${dateKey}`;
      btn.innerHTML = '<i class="bi bi-plus-circle"></i> Añadir';

      const collapse = document.createElement('div');
      collapse.className = 'collapse mt-2';
      collapse.id = `hours-add-${dateKey}`;

      const form = document.createElement('form');
      form.className = 'row g-2';
      const col = document.createElement('div');
      col.className = 'col';
      const input = document.createElement('input');
      input.type = 'time';
      input.required = true;
      input.className = 'form-control form-control-sm';
      col.appendChild(input);
      const colBtn = document.createElement('div');
      colBtn.className = 'col-auto';
      const saveB = document.createElement('button');
      saveB.type = 'submit';
      saveB.className = 'btn btn-sm btn-dark';
      saveB.textContent = 'Guardar';
      colBtn.appendChild(saveB);
      form.appendChild(col);
      form.appendChild(colBtn);
      collapse.appendChild(form);

      const list = document.createElement('ul');
      list.className = 'list-unstyled mt-2';

      form.addEventListener('submit', e => {
        e.preventDefault();
        const val = input.value;
        if (!val) return;
        if (!hoursMap[dateKey].includes(val)) hoursMap[dateKey].push(val);
        input.value = '';
        collapse.classList.remove('show');
        renderDay(list, dateKey);
        saveHours();
      });

      cell.appendChild(btn);
      cell.appendChild(collapse);
      cell.appendChild(list);
      renderDay(list, dateKey);
      row.appendChild(cell);
    }
    tbody.appendChild(row);
  }

  function syncAvailability() {
    if (!availMonth || !availYear) return;
    if (!monthSelect || !yearSelect) return;
    availMonth.value = monthSelect.value;
    availYear.value = yearSelect.value;
    availMonth.dispatchEvent(new Event('change'));
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
    syncAvailability();
  }

  if (monthSelect)
    monthSelect.addEventListener('change', () => {
      const month = parseInt(monthSelect.value, 10);
      const year = parseInt(yearSelect.value, 10);
      startDate = new Date(year, month, 1);
      if (startDate < today) startDate = new Date(today);
      renderHours();
      saveHours();
      buildTable();
      syncAvailability();
    });

  if (yearSelect)
    yearSelect.addEventListener('change', () => {
      const month = parseInt(monthSelect.value, 10);
      const year = parseInt(yearSelect.value, 10);
      startDate = new Date(year, month, 1);
      if (startDate < today) startDate = new Date(today);
      renderHours();
      saveHours();
      buildTable();
      syncAvailability();
    });

  if (prevBtn) prevBtn.addEventListener('click', () => changeDays(-1));
  if (nextBtn) nextBtn.addEventListener('click', () => changeDays(1));

  if (hoursForm) {
    hoursForm.addEventListener('submit', e => {
      e.preventDefault();
      const dateVal = dateInput.value;
      const timeVal = timeInput.value;
      if (!dateVal || !timeVal) return;
      if (!hoursMap[dateVal]) hoursMap[dateVal] = [];
      if (!hoursMap[dateVal].includes(timeVal)) hoursMap[dateVal].push(timeVal);
      dateInput.value = '';
      timeInput.value = '';
      renderHours();
      saveHours();
      buildTable();
    });
  }

  if (clearBtn) {
    clearBtn.addEventListener('click', () => {
      hoursMap = {};
      renderHours();
      saveHours();
    });
  }

  document.addEventListener('availabilityDateChange', e => {
    if (!e.detail || !e.detail.startDate) return;
    startDate = new Date(e.detail.startDate);
    buildTable();
    updateSelectors();
  });

  // sync initial position with availability controls if present
  if (availMonth && availYear) {
    startDate = new Date(parseInt(availYear.value, 10), parseInt(availMonth.value, 10), 1);
    if (startDate < today) startDate = new Date(today);
  }

  renderHours();
  saveHours();
  buildTable();
});
