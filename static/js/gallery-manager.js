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
        text.textContent = 'Arrastra imágenes aquí o haz clic para seleccionar';
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
  const selectAllBtn = document.getElementById('select-all');
  const gallery = document.getElementById('gallery-grid');
  const deleteForm = document.getElementById('bulk-delete-form');
  const deleteIds = document.getElementById('delete-ids');

  selectBtn && selectBtn.addEventListener('click', () => {
    gallery.classList.toggle('select-mode');
    if (selectAllBtn) selectAllBtn.classList.toggle('d-none');
  });

  selectAllBtn && selectAllBtn.addEventListener('click', () => {
    const boxes = gallery.querySelectorAll('.photo-checkbox');
    const allChecked = Array.from(boxes).every(cb => cb.checked);
    boxes.forEach(cb => { cb.checked = !allChecked; });
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
