document.addEventListener('DOMContentLoaded', () => {
  const input = document.getElementById('id_review_images');
  const preview = document.getElementById('reviewImagesPreview');
  const modal = document.getElementById('reviewImagesModal');
  if (!input || !preview || !modal) return;

  const modalImg = modal.querySelector('img');
  const prevBtn = modal.querySelector('[data-slide="prev"]');
  const nextBtn = modal.querySelector('[data-slide="next"]');
  let images = [];
  let idx = 0;

  const maxSize = 5 * 1024 * 1024;

  function updateModal() {
    if (!images.length) return;
    modalImg.src = images[idx];
  }

  function openModal(i) {
    idx = i;
    updateModal();
    new bootstrap.Modal(modal).show();
  }

  prevBtn.addEventListener('click', () => {
    idx = (idx - 1 + images.length) % images.length;
    updateModal();
  });
  nextBtn.addEventListener('click', () => {
    idx = (idx + 1) % images.length;
    updateModal();
  });

  input.addEventListener('change', () => {
    preview.innerHTML = '';
    images = [];
    Array.from(input.files).forEach((file, i) => {
      if (file.size > maxSize) {
        alert('El archivo supera el límite de 5MB');
        input.value = '';
        preview.innerHTML = '';
        images = [];
        return;
      }
      const reader = new FileReader();
      reader.onload = e => {
        images.push(e.target.result);
        const img = document.createElement('img');
        img.src = e.target.result;
        img.className = 'img-thumbnail m-1 review-thumb';
        img.style.height = '75px';
        img.style.width = '75px';
        img.style.objectFit = 'cover';
        img.addEventListener('click', () => openModal(images.indexOf(e.target.result)));
        preview.appendChild(img);
      };
      reader.readAsDataURL(file);
    });
  });
});

