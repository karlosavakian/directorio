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

  let schedule = {};
  if (dataEl) {
    try {
      schedule = JSON.parse(dataEl.textContent);
    } catch (e) {
      schedule = {};
    }
  }

  const DAYS_STEP = 10;
  const dayNames = ['Dom', 'Lun', 'Mar', 'Mié', 'Jue', 'Vie', 'Sáb'];
  const dayKeys = ['domingo','lunes','martes','miercoles','jueves','viernes','sabado'];
  const today = new Date();
  let startDate = new Date(today.getFullYear(), today.getMonth(), today.getDate());
  const endOfYear = new Date(today.getFullYear(), 11, 31);

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
    buildTable();
    syncAvailability();
  });

  yearSelect.addEventListener('change', () => {
    const month = parseInt(monthSelect.value, 10);
    const year = parseInt(yearSelect.value, 10);
    startDate = new Date(year, month, 1);
    if (startDate < today) startDate = new Date(today);
    buildTable();
    syncAvailability();
  });

  if (prevBtn) prevBtn.addEventListener('click', () => changeDays(-1));
  if (nextBtn) nextBtn.addEventListener('click', () => changeDays(1));

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

  buildTable();
});
