function initAvatarDropzones(context = document) {
  context.querySelectorAll('.avatar-dropzone').forEach(zone => {
    const input = zone.querySelector('input[type="file"]');
    const preview = zone.querySelector('.avatar-preview');
    const msg = preview.querySelector('.avatar-dropzone-msg');
    if (!input || !preview) return;

    const showFile = file => {
      if (!file) return;
      const reader = new FileReader();
      reader.onload = e => {
        preview.style.backgroundImage = `url('${e.target.result}')`;
        preview.classList.add('has-image');
        if (msg) msg.style.display = 'none';
      };
      reader.readAsDataURL(file);
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
  });
}

document.addEventListener('DOMContentLoaded', () => {
  initAvatarDropzones();
});

window.initAvatarDropzones = initAvatarDropzones;
