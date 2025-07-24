document.addEventListener('DOMContentLoaded', () => {
  const modalEl = document.getElementById('bookingModal');
  const modal = modalEl ? new bootstrap.Modal(modalEl) : null;
  const confirmEl = document.getElementById('confirmCancelModal');
  const confirmModal = confirmEl ? new bootstrap.Modal(confirmEl) : null;
  const bookingBtns = document.querySelectorAll('.booking-btn');
  let clubSlug = null;
  let availability = {};

  const dayPrev = modalEl?.querySelector('#days-prev');
  const dayNext = modalEl?.querySelector('#days-next');
  let days = [];
  let dayStart = 0;
  let currentDate;
  const today = new Date();

  const timeContainers = {
    morning: {start: 0, slots: []},
    afternoon: {start: 0, slots: []},
    evening: {start: 0, slots: []}
  };

  function updateMonthTitle() {
    const monthTitle = modalEl.querySelector('#booking-month-title');
    if (monthTitle) {
      monthTitle.textContent = currentDate.toLocaleDateString('es', {
        month: 'long',
        year: 'numeric'
      });
    }
  }

  function buildDays() {
    days = [];
    dayStart = 0;
    const year = currentDate.getFullYear();
    const month = currentDate.getMonth();
    const daysInMonth = new Date(year, month + 1, 0).getDate();
    const startDay = year === today.getFullYear() && month === today.getMonth() ? today.getDate() : 1;
    for (let i = startDay; i <= daysInMonth; i++) {
      const date = new Date(year, month, i);
      const dateStr = date.toISOString().split('T')[0];
      const dayName = date.toLocaleDateString('es', { weekday: 'short' });
      const card = document.createElement('div');
      card.className = 'day-card border rounded text-center p-2';
      card.style.cursor = 'pointer';
      const dayData = availability[dateStr] || {};
      const totalHours = Object.keys(dayData).length;
      const availableHours = Object.values(dayData).reduce(
        (acc, val) => acc + (val > 0 ? 1 : 0),
        0
      );
      let badgeClass;
      if (totalHours === 0) {
        badgeClass = 'bg-secondary';
      } else if (availableHours === 0) {
        badgeClass = 'bg-danger';
      } else if (availableHours > 2) {
        badgeClass = 'bg-success';
      } else {
        badgeClass = 'bg-warning text-dark';
      }
      card.innerHTML =
        `<div class="small">${dayName.charAt(0).toUpperCase() + dayName.slice(1)}</div>` +
        `<div class="fw-bold">${i}</div>` +
        `<span class="badge ${badgeClass}"></span>`;
      card.dataset.date = dateStr;
      if (availableHours === 0) {
        card.classList.add('disabled');
      } else {
        card.addEventListener('click', () => {
          modalEl.querySelectorAll('.day-card.active').forEach(d => d.classList.remove('active'));
          card.classList.add('active');
          loadTimes(dateStr);
        });
      }
      days.push(card);
    }
  }

  function renderDays() {
    const container = modalEl.querySelector('#booking-days');
    container.innerHTML = '';
    const visible = days.slice(dayStart, dayStart + 7);
    visible.forEach(card => container.appendChild(card));
    const startOfToday = new Date(today.getFullYear(), today.getMonth(), 1);
    const prevAvailable = dayStart > 0 || currentDate > startOfToday;
    if (dayPrev) dayPrev.disabled = !prevAvailable;
    if (dayNext) dayNext.disabled = false;
  }

  function renderTimes() {
    let firstVisible = null;
    ['morning', 'afternoon', 'evening'].forEach(key => {
      const info = timeContainers[key];
      const container = modalEl.querySelector(`#${key}-slots`);
      container.innerHTML = '';
      info.slots.slice(info.start, info.start + 7).forEach(btn => container.appendChild(btn));

      const prev = modalEl.querySelector(`.time-prev[data-target="${key}"]`);
      const next = modalEl.querySelector(`.time-next[data-target="${key}"]`);
      if (prev) prev.disabled = info.start === 0;
      if (next) next.disabled = info.start + 7 >= info.slots.length;

      const tabBtn = modalEl.querySelector(`#${key}-tab`);
      const tabItem = tabBtn?.closest('.nav-item');
      const pane = modalEl.querySelector(`#${key}`);
      if (info.slots.length === 0) {
        tabItem?.classList.add('d-none');
        pane?.classList.add('d-none');
      } else {
        tabItem?.classList.remove('d-none');
        pane?.classList.remove('d-none');
        if (!firstVisible) firstVisible = key;
      }
    });

    let activeKey = ['morning', 'afternoon', 'evening'].find(k => {
      const btn = modalEl.querySelector(`#${k}-tab`);
      return btn && btn.classList.contains('active') && !btn.closest('.nav-item').classList.contains('d-none');
    });

    if (!activeKey) activeKey = firstVisible;

    modalEl.querySelectorAll('#timeTabs .nav-link').forEach(btn => btn.classList.remove('active'));
    modalEl.querySelectorAll('.tab-pane').forEach(pane => pane.classList.remove('show', 'active'));

    if (activeKey) {
      modalEl.querySelector(`#${activeKey}-tab`)?.classList.add('active');
      const pane = modalEl.querySelector(`#${activeKey}`);
      pane?.classList.add('show', 'active');
    }
  }

  function loadTimes(dateStr) {
    Object.values(timeContainers).forEach(info => { info.slots = []; info.start = 0; });

    function createSlot(time) {
      const button = document.createElement('button');
      button.type = 'button';
      button.className = 'btn btn-outline-dark btn-sm slot-btn';
      button.textContent = time;
      button.addEventListener('click', () => {
        modalEl.querySelectorAll('.slot-btn.active').forEach(b => b.classList.remove('active'));
        button.classList.add('active');
      });
      return button;
    }

    const dayData = availability[dateStr] || {};
    Object.keys(dayData).sort().forEach(time => {
      if (dayData[time] > 0) {
        const [h] = time.split(':').map(Number);
        const btn = createSlot(time);
        if (h < 12) timeContainers.morning.slots.push(btn);
        else if (h < 18) timeContainers.afternoon.slots.push(btn);
        else timeContainers.evening.slots.push(btn);
      }
    });
    renderTimes();
  }

  function selectFirstAvailable() {
    const first = days.find(d => !d.classList.contains('disabled'));
    if (first) {
      modalEl.querySelectorAll('.day-card.active').forEach(d => d.classList.remove('active'));
      first.classList.add('active');
      loadTimes(first.dataset.date);
    } else {
      Object.values(timeContainers).forEach(info => { info.slots = []; info.start = 0; });
      renderTimes();
    }
  }

  function populateModal() {
    if (!modalEl) return;
    try {
      availability = JSON.parse(localStorage.getItem('availability-' + clubSlug)) || {};
    } catch { availability = {}; }

    currentDate = new Date(today.getFullYear(), today.getMonth(), 1);
    updateMonthTitle();
    buildDays();
    renderDays();

    selectFirstAvailable();
  }

  if (modal) {
    bookingBtns.forEach(btn => {
      btn.addEventListener('click', () => {
        clubSlug = btn.dataset.clubSlug;
        populateModal();
        modal.show();
        modalEl.querySelectorAll('[data-bs-toggle="tooltip"]').forEach(el => new bootstrap.Tooltip(el));
      });
    });

    if (dayPrev) {
      dayPrev.addEventListener('click', () => {
        if (dayStart > 0) {
          dayStart -= 7;
        } else {
          const prevMonth = new Date(currentDate.getFullYear(), currentDate.getMonth() - 1, 1);
          const startOfToday = new Date(today.getFullYear(), today.getMonth(), 1);
          if (prevMonth >= startOfToday) {
            currentDate = prevMonth;
            updateMonthTitle();
            buildDays();
            dayStart = Math.max(0, days.length - 7);
          }
        }
        renderDays();
        selectFirstAvailable();
      });
    }
    if (dayNext) {
      dayNext.addEventListener('click', () => {
        if (dayStart + 7 < days.length) {
          dayStart += 7;
        } else {
          currentDate.setMonth(currentDate.getMonth() + 1);
          updateMonthTitle();
          buildDays();
        }
        renderDays();
        selectFirstAvailable();
      });
    }

    modalEl.querySelectorAll('.time-prev').forEach(btn => {
      btn.addEventListener('click', () => {
        const key = btn.dataset.target;
        const info = timeContainers[key];
        if (info.start > 0) { info.start -= 7; renderTimes(); }
      });
    });
    modalEl.querySelectorAll('.time-next').forEach(btn => {
      btn.addEventListener('click', () => {
        const key = btn.dataset.target;
        const info = timeContainers[key];
        if (info.start + 7 < info.slots.length) { info.start += 7; renderTimes(); }
      });
    });

    if (confirmModal) {
      const confirmBtn = confirmEl.querySelector('.confirm-cancel');
      if (confirmBtn) {
        confirmBtn.addEventListener('click', () => {
          modalEl.dataset.forced = 'true';
          confirmModal.hide();
          modal.hide();
        });
      }
    }

    modalEl.addEventListener('hide.bs.modal', e => {
      if (!modalEl.dataset.forced && confirmModal) {
        e.preventDefault();
        confirmModal.show();
      }
    });

    modalEl.addEventListener('hidden.bs.modal', () => {
      delete modalEl.dataset.forced;
    });

    const classCards = modalEl.querySelectorAll('.class-card');
    classCards.forEach(card => {
      const radio = card.querySelector('input[type="radio"]');
      if (radio.checked) card.classList.add('active');
      card.addEventListener('click', () => {
        radio.checked = true;
        classCards.forEach(c => c.classList.remove('active'));
        card.classList.add('active');
      });
    });

    const form = modalEl.querySelector('#booking-form');
    form.addEventListener('submit', async e => {
      e.preventDefault();
      const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]')?.value;
      const dayCard = modalEl.querySelector('.day-card.active');
      const slotBtn = modalEl.querySelector('.slot-btn.active');
      if (!clubSlug || !dayCard || !slotBtn) return;
      const data = new URLSearchParams();
      data.append('date', dayCard.dataset.date);
      data.append('time', slotBtn.textContent);
      const tipoRadio = modalEl.querySelector('input[name="clase_id"]:checked');
      if (tipoRadio) data.append('clase_id', tipoRadio.value);
      const res = await fetch(`/clubs/${clubSlug}/reservar/crear/`, {
        method: 'POST',
        headers: {
          'X-CSRFToken': csrftoken,
          'X-Requested-With': 'XMLHttpRequest'
        },
        credentials: 'same-origin',
        body: data
      });
      if (res.ok) {
        showToast('Reserva completada');
      }
      modalEl.dataset.forced = 'true';
      modal.hide();
    });
  }
});

function showToast(message) {
  let container = document.querySelector('.toast-container');
  if (!container) {
    container = document.createElement('div');
    container.className = 'toast-container position-fixed top-0 end-0 p-3';
    document.body.appendChild(container);
  }
  const toast = document.createElement('div');
  toast.className = 'toast bg-black text-bg-success border-0 mb-2';
  toast.role = 'alert';
  toast.innerHTML = `<div class="d-flex"><div class="toast-body">${message}</div>` +
                    `<button type="button" class="btn-close btn-close-white me-2 m-auto" data-bs-dismiss="toast" aria-label="Close"></button></div>`;
  container.appendChild(toast);
  new bootstrap.Toast(toast).show();
}
