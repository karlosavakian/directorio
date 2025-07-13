document.addEventListener('DOMContentLoaded', () => {
  const uploadForm = document.getElementById('upload-form');
  const uploadInput = document.getElementById('id_gallery_image');
  const addBtn = document.getElementById('add-photos-btn');

  if (addBtn && uploadInput && uploadForm) {
    addBtn.addEventListener('click', () => uploadInput.click());
    uploadInput.addEventListener('change', () => {
      if (uploadInput.files.length) {
        uploadForm.submit();
      }
    });
  }

  const gallery = document.getElementById('gallery-grid');
  const deleteForm = document.getElementById('bulk-delete-form');
  const deleteIds = document.getElementById('delete-ids');
  const selectAllBtn = document.getElementById('select-all');
  const deselectAllBtn = document.getElementById('deselect-all');
  const deleteBtn = deleteForm && deleteForm.querySelector('button[type="submit"]');

  const updateActionStates = () => {
    if (!gallery) return;
    const anyChecked = gallery.querySelectorAll('.photo-checkbox:checked').length > 0;
    if (anyChecked) {
      deselectAllBtn && deselectAllBtn.classList.remove('text-muted');
      deselectAllBtn && deselectAllBtn.classList.add('text-dark');
      deleteBtn && deleteBtn.classList.remove('text-muted');
      deleteBtn && deleteBtn.classList.add('text-dark');
    } else {
      deselectAllBtn && deselectAllBtn.classList.add('text-muted');
      deselectAllBtn && deselectAllBtn.classList.remove('text-dark');
      deleteBtn && deleteBtn.classList.add('text-muted');
      deleteBtn && deleteBtn.classList.remove('text-dark');
    }
  };

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

    gallery.querySelectorAll('.photo-checkbox').forEach(cb => {
      cb.addEventListener('change', updateActionStates);
    });
  }

  selectAllBtn && selectAllBtn.addEventListener('click', () => {
    gallery && gallery
      .querySelectorAll('.photo-checkbox')
      .forEach(cb => {
        cb.checked = true;
      });
    updateActionStates();
  });

  deselectAllBtn && deselectAllBtn.addEventListener('click', () => {
    gallery && gallery
      .querySelectorAll('.photo-checkbox')
      .forEach(cb => {
        cb.checked = false;
      });
    updateActionStates();
  });

  deleteForm && deleteForm.addEventListener('submit', e => {
    const ids = [...gallery.querySelectorAll('.photo-checkbox:checked')].map(cb => cb.value);
    if (!ids.length) {
      e.preventDefault();
      return;
    }
    deleteIds.value = ids.join(',');
  });

  updateActionStates();
});
