document.addEventListener('DOMContentLoaded', () => {
  document.querySelectorAll('.photo-dropzone').forEach(zone => {
    const input = zone.querySelector('input[type="file"]');
    const msg = zone.querySelector('.photo-dropzone-msg');
    const text = msg && msg.querySelector('span');
    if (!input || !msg || !text) return;
    const showCount = () => {
      if (input.files.length) {
        text.textContent = `${input.files.length} archivo(s) seleccionado(s)`;
      } else {
        text.textContent = 'Haz clic para seleccionar imágenes';
      }
    };
    zone.addEventListener('click', () => input.click());
    input.addEventListener('change', showCount);
  });

  const gallery = document.getElementById('gallery-grid');
  const deleteForm = document.getElementById('bulk-delete-form');
  const deleteIds = document.getElementById('delete-ids');

  let dragged = null;
  if (gallery) {
    gallery.addEventListener('dragstart', e => {
      const item = e.target.closest('.gallery-item');
      if (item) {
        dragged = item;
      }
    });

    gallery.addEventListener('dragover', e => {
      e.preventDefault();
      const target = e.target.closest('.gallery-item');
      if (dragged && target && target !== dragged) {
        const rect = target.getBoundingClientRect();
        const next = (e.clientY - rect.top) / (rect.bottom - rect.top) > 0.5;
        gallery.insertBefore(dragged, next ? target.nextSibling : target);
      }
    });

    gallery.addEventListener('drop', e => {
      e.preventDefault();
      dragged = null;
    });
  }

  deleteForm && deleteForm.addEventListener('submit', e => {
    const ids = [...gallery.querySelectorAll('.photo-checkbox:checked')].map(cb => cb.value);
    if (!ids.length) {
      e.preventDefault();
      return;
    }
    deleteIds.value = ids.join(',');
  });
});
