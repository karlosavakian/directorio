document.addEventListener('DOMContentLoaded', () => {
  const imgInput = document.getElementById('id_image');
  const imgPreview = document.getElementById('imagePreview');
  if (imgInput && imgPreview) {
    const updatePreview = () => {
      const file = imgInput.files && imgInput.files[0];
      if (file) {
        const reader = new FileReader();
        reader.onload = e => {
          imgPreview.src = e.target.result;
          imgPreview.classList.remove('d-none');
        };
        reader.readAsDataURL(file);
      } else {
        imgPreview.src = '';
        imgPreview.classList.add('d-none');
      }
    };
    imgInput.addEventListener('change', updatePreview);
  }

  const textarea = document.getElementById('id_contenido');
  const ytPreview = document.getElementById('youtubePreview');
  if (textarea && ytPreview) {
    const pattern = /(https?:\/\/(?:www\.)?(?:youtube\.com\/watch\?v=|youtu\.be\/)([\w-]+))/;
    const updateYoutube = () => {
      const match = textarea.value.match(pattern);
      if (match) {
        ytPreview.src = `https://img.youtube.com/vi/${match[2]}/hqdefault.jpg`;
        ytPreview.classList.remove('d-none');
      } else {
        ytPreview.src = '';
        ytPreview.classList.add('d-none');
      }
    };
    textarea.addEventListener('input', updateYoutube);
    updateYoutube();
  }
});
