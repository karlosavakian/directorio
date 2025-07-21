document.addEventListener('DOMContentLoaded', () => {
  const modalEl = document.getElementById('bookingModal');
  const modal = modalEl ? new bootstrap.Modal(modalEl) : null;
  const btn = document.querySelector('.booking-btn');

  function populateModal() {
    if (!modalEl) return;

    const now = new Date();
    const monthTitle = modalEl.querySelector('#booking-month-title');
    monthTitle.textContent = now.toLocaleDateString('es', {
      month: 'long',
      year: 'numeric'
    });

    const daysContainer = modalEl.querySelector('#booking-days');
    daysContainer.innerHTML = '';
    const daysInMonth = new Date(now.getFullYear(), now.getMonth() + 1, 0).getDate();
    for (let i = 1; i <= daysInMonth; i++) {
      const date = new Date(now.getFullYear(), now.getMonth(), i);
      const dayName = date.toLocaleDateString('es', { weekday: 'short' });
      const card = document.createElement('div');
      card.className = 'day-card border rounded text-center p-2';
      const badgeClass = Math.random() > 0.5 ? 'bg-success' : 'bg-danger';
      card.innerHTML =
        `<div class="small">${dayName.charAt(0).toUpperCase() + dayName.slice(1)}</div>` +
        `<div class="fw-bold">${i}</div>` +
        `<span class="badge ${badgeClass}"></span>`;
      daysContainer.appendChild(card);
    }

    const morning = modalEl.querySelector('#morning-slots');
    const afternoon = modalEl.querySelector('#afternoon-slots');
    const evening = modalEl.querySelector('#evening-slots');
    [morning, afternoon, evening].forEach(c => c.innerHTML = '');

    function addSlot(container, time) {
      const button = document.createElement('button');
      button.type = 'button';
      button.className = 'btn btn-outline-dark btn-sm slot-btn';
      button.textContent = time;
      button.addEventListener('click', () => {
        modalEl.querySelectorAll('.slot-btn.active').forEach(b => b.classList.remove('active'));
        button.classList.add('active');
      });
      container.appendChild(button);
    }

    for (let h = 0; h < 24; h++) {
      for (let m = 0; m < 60; m += 30) {
        const time = `${String(h).padStart(2, '0')}:${String(m).padStart(2, '0')}`;
        if (h < 12) addSlot(morning, time);
        else if (h < 18) addSlot(afternoon, time);
        else addSlot(evening, time);
      }
    }
  }

  if (btn && modal) {
    btn.addEventListener('click', () => {
      populateModal();
      modal.show();
    });

    const form = modalEl.querySelector('#booking-form');
    form.addEventListener('submit', e => {
      e.preventDefault();
      modal.hide();
    });
  }
});
