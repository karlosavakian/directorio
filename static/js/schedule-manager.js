// static/js/schedule-manager.js

document.addEventListener('DOMContentLoaded', () => {
  const table = document.getElementById('schedule-table');
  if (!table) return;
  const dataEl = document.getElementById('schedule-data');
  const monthSelect = document.getElementById('schedule-month');
  const yearSelect = document.getElementById('schedule-year');
  const prevBtn = document.getElementById('schedule-prev');
  const nextBtn = document.getElementById('schedule-next');
  const availMonth = document.getElementById('availability-month');
  const availYear = document.getElementById('availability-year');
  const hoursForm = document.getElementById('schedule-hours-form');
  const hoursStart = document.getElementById('schedule-hours-start');
  const hoursEnd = document.getElementById('schedule-hours-end');
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

  const getHoursKey = () => `schedule-hours-${yearSelect.value}-${monthSelect.value}`;

  let hours = [];
  function loadHours() {
    try {
      hours = JSON.parse(localStorage.getItem(getHoursKey())) || [];
    } catch {
      hours = [];
    }
  }
  loadHours();

  const DAYS_STEP = 10;
  const dayNames = ['Dom', 'Lun', 'Mar', 'Mié', 'Jue', 'Vie', 'Sáb'];
  const dayKeys = ['domingo','lunes','martes','miercoles','jueves','viernes','sabado'];
  const today = new Date();
  let startDate = new Date(today.getFullYear(), today.getMonth(), today.getDate());
  const endOfYear = new Date(today.getFullYear(), 11, 31);

  function renderHours() {
    if (!hoursList) return;
    hoursList.innerHTML = '';
    hours.sort().forEach((t, idx) => {
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
        if (hours.includes(val) && val !== t) {
          form.style.display = 'none';
          return;
        }
        hours[idx] = val;
        renderHours();
        saveHours();
      });

      delBtn.addEventListener('click', () => {
        hours = hours.filter(h => h !== t);
        renderHours();
        saveHours();
      });

      hoursList.appendChild(li);
    });
  }

  function saveHours() {
    localStorage.setItem(getHoursKey(), JSON.stringify(hours));
    document.dispatchEvent(new CustomEvent('scheduleHoursUpdate', { detail: { hours } }));
  }

  function updateSelectors() {
    monthSelect.value = startDate.getMonth();
    yearSelect.value = startDate.getFullYear();
  }

  function buildTable() {
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
      const key = dayKeys[date.getDay()];
      const cell = document.createElement('td');
      cell.style.verticalAlign = 'top';
      const blocks = schedule[key] || [];
      if (!blocks.length) {
        const small = document.createElement('small');
        small.className = 'text-muted';
        small.textContent = 'Sin horarios';
        cell.appendChild(small);
      } else {
        blocks.forEach(b => {
          const div = document.createElement('div');
          div.className = 'small fw-medium border rounded p-1 mb-1';
          if (b.estado === 'abierto') {
            const span = document.createElement('span');
            span.className = 'schedule-item';
            span.dataset.start = b.hora_inicio;
            span.dataset.end = b.hora_fin;
            span.textContent = `${b.hora_inicio} - ${b.hora_fin}`;
            div.appendChild(span);
          } else if (b.estado === 'cerrado') {
            const span = document.createElement('span');
            span.className = 'text-danger';
            span.textContent = 'Cerrado';
            div.appendChild(span);
          } else {
            const span = document.createElement('span');
            span.className = 'text-muted';
            span.textContent = b.estado_otro;
            div.appendChild(span);
          }
          cell.appendChild(div);
        });
      }
      row.appendChild(cell);
    }
    tbody.appendChild(row);
  }

  function syncAvailability() {
    if (!availMonth || !availYear) return;
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

  monthSelect.addEventListener('change', () => {
    const month = parseInt(monthSelect.value, 10);
    const year = parseInt(yearSelect.value, 10);
    startDate = new Date(year, month, 1);
    if (startDate < today) startDate = new Date(today);
    loadHours();
    renderHours();
    saveHours();
    buildTable();
    syncAvailability();
  });

  yearSelect.addEventListener('change', () => {
    const month = parseInt(monthSelect.value, 10);
    const year = parseInt(yearSelect.value, 10);
    startDate = new Date(year, month, 1);
    if (startDate < today) startDate = new Date(today);
    loadHours();
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
      const start = hoursStart.value;
      const end = hoursEnd.value;
      if (start && !hours.includes(start)) hours.push(start);
      if (end && !hours.includes(end)) hours.push(end);
      hoursStart.value = '';
      hoursEnd.value = '';
      renderHours();
      saveHours();
    });
  }

  if (clearBtn) {
    clearBtn.addEventListener('click', () => {
      hours = [];
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

  loadHours();
  renderHours();
  saveHours();

  buildTable();
});
