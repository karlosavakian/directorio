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

  const uploadForm = document.getElementById('upload-form');
  const uploadInput = document.getElementById('id_gallery_image');
  const uploadBtn = document.getElementById('add-photos-btn');

  if (uploadForm && uploadInput && uploadBtn) {
    uploadBtn.addEventListener('click', () => uploadInput.click());
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

  const updateActionStyles = () => {
    const hasSelected =
      gallery && gallery.querySelectorAll('.photo-checkbox:checked').length > 0;
    if (deselectAllBtn) {
      deselectAllBtn.classList.toggle('text-secondary', !hasSelected);
      deselectAllBtn.classList.toggle('text-black', hasSelected);
    }
    if (deleteBtn) {
      deleteBtn.classList.toggle('text-secondary', !hasSelected);
      deleteBtn.classList.toggle('text-danger', hasSelected);
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
  }

  selectAllBtn && selectAllBtn.addEventListener('click', () => {
    gallery &&
      gallery.querySelectorAll('.photo-checkbox').forEach(cb => {
        cb.checked = true;
      });
    updateActionStyles();
  });

  deselectAllBtn && deselectAllBtn.addEventListener('click', () => {
    gallery &&
      gallery.querySelectorAll('.photo-checkbox').forEach(cb => {
        cb.checked = false;
      });
    updateActionStyles();
  });

  deleteForm && deleteForm.addEventListener('submit', e => {
    const ids = [...gallery.querySelectorAll('.photo-checkbox:checked')].map(
      cb => cb.value
    );
    if (!ids.length) {
      e.preventDefault();
      return;
    }
    deleteIds.value = ids.join(',');
  });

  gallery &&
    gallery.querySelectorAll('.photo-checkbox').forEach(cb =>
      cb.addEventListener('change', updateActionStyles)
    );

  updateActionStyles();

  gallery &&
    gallery.querySelectorAll('.gallery-item img').forEach(img => {
      const overlay = img.parentElement.querySelector('.photo-size');
      if (!overlay) return;
      const setSize = () => {
        overlay.textContent = `${img.naturalWidth}x${img.naturalHeight}`;
      };
      if (img.complete) {
        setSize();
      } else {
        img.addEventListener('load', setSize);
      }
    });
});
