function initAvatarDropzones(root = document) {
  root.querySelectorAll('.avatar-dropzone').forEach(zone => {
    if (zone.dataset.initialized) return;
    const input = zone.querySelector('input[type="file"]');
    const preview = zone.querySelector('.avatar-preview');
    const msg = preview.querySelector('.avatar-dropzone-msg');
    const removeBtn = document.createElement('button');
    removeBtn.type = 'button';
    removeBtn.className = 'avatar-remove-btn';
    removeBtn.innerHTML = '<i class="bi bi-trash"></i>';
    zone.appendChild(removeBtn);
    if (!input || !preview) return;

    const showFile = file => {
      if (!file) return;
      const reader = new FileReader();
      reader.onload = e => {
        preview.style.backgroundImage = `url('${e.target.result}')`;
        preview.classList.add('has-image');
        if (msg) msg.style.visibility = 'hidden';
        updateState();
      };
      reader.readAsDataURL(file);
    };

    const clearFile = () => {
      input.value = '';
      preview.style.backgroundImage = '';
      preview.classList.remove('has-image');
      if (msg) msg.style.visibility = '';
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
        showFile(input.files[0]);
      }
    });

    updateState();
    zone.dataset.initialized = 'true';
  });
}

document.addEventListener('DOMContentLoaded', () => {
  initAvatarDropzones();
});

window.initAvatarDropzones = initAvatarDropzones;
