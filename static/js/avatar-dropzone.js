function initAvatarDropzones(root = document) {
  root.querySelectorAll('.avatar-dropzone').forEach(zone => {
    if (zone.dataset.initialized) return;
    const input = zone.querySelector('input[type="file"]');
    const preview = zone.querySelector('.avatar-preview');
    const clearCheckbox = zone.querySelector('input[type="checkbox"]');
    const clearLabel = clearCheckbox ? zone.querySelector(`label[for='${clearCheckbox.id}']`) : null;

    // Remove default Django ClearableFileInput elements
    zone.querySelectorAll('a, br').forEach(el => el.remove());
    if (clearLabel) clearLabel.remove();
    Array.from(zone.childNodes).forEach(node => {
      if (node.nodeType === Node.TEXT_NODE && node.textContent.trim()) {
        node.remove();
      }
    });
    if (clearCheckbox) clearCheckbox.classList.add('d-none');

    const msg = preview.querySelector('.avatar-dropzone-msg');
    const removeBtn = document.createElement('button');
    removeBtn.type = 'button';
    removeBtn.className = 'avatar-remove-btn';
    removeBtn.innerHTML = '<i class="bi bi-trash"></i>';
    zone.appendChild(removeBtn);
    const loader = document.createElement('div');
    loader.className = 'dropzone-loader d-none';
    loader.innerHTML =
      '<div class="spinner-border" role="status"><span class="visually-hidden">Cargando...</span></div>';
    preview.appendChild(loader);

    if (!input || !preview) return;

    const showFile = file => {
      if (!file) return;
      loader.classList.remove('d-none');
      const reader = new FileReader();
      reader.onload = e => {
        preview.style.backgroundImage = `url('${e.target.result}')`;
        preview.classList.add('has-image');
        if (msg) msg.style.visibility = 'hidden';
        updateState();
        loader.classList.add('d-none');
      };
      reader.onerror = () => loader.classList.add('d-none');
      reader.readAsDataURL(file);
    };

    const clearFile = () => {
      input.value = '';
      preview.style.backgroundImage = '';
      preview.classList.remove('has-image');
      if (clearCheckbox) clearCheckbox.checked = true;
      if (msg) msg.style.visibility = '';
      loader.classList.add('d-none');
      updateState();
    };

    removeBtn.addEventListener('click', e => {
      e.stopPropagation();
      clearFile();
    });

    const updateState = () => {
      removeBtn.style.display = preview.classList.contains('has-image') ? 'flex' : 'none';
    };

    zone.addEventListener('click', () => input.click());

    zone.addEventListener('dragover', e => {
      e.preventDefault();
      zone.classList.add('dragover');
    });

    zone.addEventListener('dragleave', () => {
      zone.classList.remove('dragover');
    });

    zone.addEventListener('drop', e => {
      e.preventDefault();
      zone.classList.remove('dragover');
      const file = e.dataTransfer.files[0];
      if (file) {
        input.files = e.dataTransfer.files;
        showFile(file);
      }
    });

    input.addEventListener('change', () => {
      if (input.files.length) {
        if (clearCheckbox) clearCheckbox.checked = false;
        showFile(input.files[0]);
      }
    });

    updateState();
    const form = zone.closest('form');
    if (form) {
      form.addEventListener('submit', () => {
        if (input.files.length) {
          loader.classList.remove('d-none');
        }
      });
    }
    zone.dataset.initialized = 'true';
  });
}

document.addEventListener('DOMContentLoaded', () => {
  initAvatarDropzones();
});

window.initAvatarDropzones = initAvatarDropzones;
