document.addEventListener('DOMContentLoaded', () => {
  document.querySelectorAll('.photo-dropzone').forEach(zone => {
    const input = zone.querySelector('input[type="file"]');
    const msg = zone.querySelector('.photo-dropzone-msg');
    if (!input || !msg) return;
    const showCount = () => {
      if (input.files.length) {
        msg.textContent = `${input.files.length} archivo(s) seleccionado(s)`;
      } else {
        msg.textContent = 'Arrastra imágenes aquí o haz clic para seleccionar';
      }
    };
    zone.addEventListener('click', () => input.click());
    zone.addEventListener('dragover', e => {
      e.preventDefault();
      zone.classList.add('dragover');
    });
    zone.addEventListener('dragleave', () => zone.classList.remove('dragover'));
    zone.addEventListener('drop', e => {
      e.preventDefault();
      zone.classList.remove('dragover');
      input.files = e.dataTransfer.files;
      showCount();
    });
    input.addEventListener('change', showCount);
  });

  const selectBtn = document.getElementById('toggle-select');
  const gallery = document.getElementById('gallery-grid');
  const deleteForm = document.getElementById('bulk-delete-form');
  const deleteIds = document.getElementById('delete-ids');

  selectBtn && selectBtn.addEventListener('click', () => {
    gallery.classList.toggle('select-mode');
  });

  deleteForm && deleteForm.addEventListener('submit', e => {
    const ids = [...gallery.querySelectorAll('.photo-checkbox:checked')].map(cb => cb.value);
    if (!ids.length) {
      e.preventDefault();
      return;
    }
    deleteIds.value = ids.join(',');
  });
});
