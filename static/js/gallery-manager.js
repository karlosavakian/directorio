document.addEventListener('DOMContentLoaded', () => {
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

  if (gallery) {
    const reorderUrl = gallery.dataset.reorderUrl;
    const csrf = document.querySelector('[name=csrfmiddlewaretoken]').value;

    gallery.querySelectorAll('.gallery-item').forEach(item => {
      const img = item.querySelector('img');
      const size = item.querySelector('.photo-size');
      if (img && size) {
        const setSize = () => {
          size.textContent = `${img.naturalWidth}px × ${img.naturalHeight}px`;
        };
        if (img.complete) setSize();
        else img.addEventListener('load', setSize);
      }
      item.setAttribute('draggable', 'true');
      item.addEventListener('dragstart', () => item.classList.add('dragging'));
      item.addEventListener('dragend', () => {
        item.classList.remove('dragging');
        const order = [...gallery.querySelectorAll('.gallery-item')].map(el => el.dataset.id);
        fetch(reorderUrl, {
          method: 'POST',
          headers: { 'Content-Type': 'application/x-www-form-urlencoded', 'X-CSRFToken': csrf },
          body: 'ids=' + order.join(',')
        });
      });
    });

    gallery.addEventListener('dragover', e => {
      e.preventDefault();
      const dragging = gallery.querySelector('.dragging');
      const after = getDragAfterElement(gallery, e.clientY);
      if (after == null) {
        gallery.appendChild(dragging);
      } else {
        gallery.insertBefore(dragging, after);
      }
    });
  }

  function getDragAfterElement(container, y) {
    const els = [...container.querySelectorAll('.gallery-item:not(.dragging)')];
    return els.reduce((closest, child) => {
      const box = child.getBoundingClientRect();
      const offset = y - box.top - box.height / 2;
      if (offset < 0 && offset > closest.offset) {
        return { offset: offset, element: child };
      } else {
        return closest;
      }
    }, { offset: Number.NEGATIVE_INFINITY }).element;
  }
});
