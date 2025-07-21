document.addEventListener('DOMContentLoaded', () => {
  const modalEl = document.getElementById('bookingModal');
  const modal = modalEl ? new bootstrap.Modal(modalEl) : null;
  const confirmEl = document.getElementById('confirmCancelModal');
  const confirmModal = confirmEl ? new bootstrap.Modal(confirmEl) : null;
  const bookingBtns = document.querySelectorAll('.booking-btn');
  let clubSlug = null;

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
      const dayName = date.toLocaleDateString('es', { weekday: 'short' });
      const card = document.createElement('div');
      card.className = 'day-card border rounded text-center p-2';
      card.style.cursor = 'pointer';
      const badgeClass = Math.random() > 0.5 ? 'bg-success' : 'bg-danger';
      card.innerHTML =
        `<div class="small">${dayName.charAt(0).toUpperCase() + dayName.slice(1)}</div>` +
        `<div class="fw-bold">${i}</div>` +
        `<span class="badge ${badgeClass}"></span>`;
      card.dataset.date = date.toISOString().split('T')[0];
      const badge = card.querySelector('.badge');
      if (!badge.classList.contains('bg-success')) {
        card.classList.add('disabled');
      } else {
        card.addEventListener('click', () => {
          modalEl.querySelectorAll('.day-card.active').forEach(d => d.classList.remove('active'));
          card.classList.add('active');
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
    ['morning', 'afternoon', 'evening'].forEach(key => {
      const info = timeContainers[key];
      const container = modalEl.querySelector(`#${key}-slots`);
      container.innerHTML = '';
      info.slots.slice(info.start, info.start + 7).forEach(btn => container.appendChild(btn));
      const prev = modalEl.querySelector(`.time-prev[data-target="${key}"]`);
      const next = modalEl.querySelector(`.time-next[data-target="${key}"]`);
      if (prev) prev.disabled = info.start === 0;
      if (next) next.disabled = info.start + 7 >= info.slots.length;
    });
  }

  function populateModal() {
    if (!modalEl) return;
    currentDate = new Date(today.getFullYear(), today.getMonth(), 1);
    updateMonthTitle();
    buildDays();
    renderDays();

    Object.values(timeContainers).forEach(info => {info.slots = []; info.start = 0;});

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

    for (let h = 0; h < 24; h++) {
      for (let m = 0; m < 60; m += 30) {
        const time = `${String(h).padStart(2, '0')}:${String(m).padStart(2, '0')}`;
        const btn = createSlot(time);
        if (h < 12) timeContainers.morning.slots.push(btn);
        else if (h < 18) timeContainers.afternoon.slots.push(btn);
        else timeContainers.evening.slots.push(btn);
      }
    }

    renderTimes();
  }

  if (modal) {
    bookingBtns.forEach(btn => {
      btn.addEventListener('click', () => {
        clubSlug = btn.dataset.clubSlug;
        populateModal();
        modal.show();
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
      const tipoRadio = modalEl.querySelector('input[name="tipo_clase"]:checked');
      if (tipoRadio) data.append('tipo_clase', tipoRadio.value);
      await fetch(`/clubs/${clubSlug}/reservar/crear/`, {
        method: 'POST',
        headers: {
          'X-CSRFToken': csrftoken,
          'X-Requested-With': 'XMLHttpRequest'
        },
        credentials: 'same-origin',
        body: data
      });
      modal.hide();
    });
  }
});
