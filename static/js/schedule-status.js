document.addEventListener('DOMContentLoaded', () => {
  const dayMap = ['domingo','lunes','martes','miercoles','jueves','viernes','sabado'];
  const now = new Date();
  const currentDay = dayMap[now.getDay()];
  const currentMinutes = now.getHours() * 60 + now.getMinutes();
  const statusEl = document.getElementById('open-status');
  const cell = document.querySelector(`td[data-day="${currentDay}"]`);
  let openNow = false;

  if (cell) {
    const items = cell.querySelectorAll('.schedule-item');
    items.forEach((item) => {
      const start = item.dataset.start;
      const end = item.dataset.end;
      if (start && end) {
        const [sh, sm] = start.split(':').map(Number);
        const [eh, em] = end.split(':').map(Number);
        const startMin = sh * 60 + sm;
        const endMin = eh * 60 + em;
        if (currentMinutes >= startMin && currentMinutes <= endMin) {
          openNow = true;
          item.classList.add('bg-success-subtle', 'fw-bold');
          item.classList.remove('text-muted');
        }
      }
    });
  }

  if (statusEl) {
    if (openNow) {
      statusEl.textContent = 'Abierto ahora';
      statusEl.classList.add('text-success');
    } else {
      statusEl.textContent = 'Cerrado ahora';
      statusEl.classList.add('text-danger');
    }
  }
});
