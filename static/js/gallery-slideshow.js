let galleryCurrent = 0;
let galleryAutoplay = null;

function updateGallery() {
  const slides = document.querySelectorAll('.gallery-slide');
  slides.forEach((slide, index) => {
    slide.classList.toggle('active', index === galleryCurrent);
  });
  const prevBtn = document.getElementById('galleryPrev');
  const nextBtn = document.getElementById('galleryNext');
  if (prevBtn && nextBtn) {
    prevBtn.style.display = galleryCurrent > 0 ? 'block' : 'none';
    nextBtn.style.display = galleryCurrent < slides.length - 1 ? 'block' : 'none';
  }
}

function changeGallery(direction) {
  const slides = document.querySelectorAll('.gallery-slide');
  galleryCurrent = (galleryCurrent + direction + slides.length) % slides.length;
  updateGallery();
}

function startGalleryAutoplay() {
  galleryAutoplay = setInterval(() => changeGallery(1), 5000);
}

function stopGalleryAutoplay() {
  clearInterval(galleryAutoplay);
}

document.addEventListener('DOMContentLoaded', () => {
  updateGallery();
  startGalleryAutoplay();
  const carousel = document.querySelector('.gallery-carousel');
  if (carousel) {
    carousel.addEventListener('mouseenter', stopGalleryAutoplay);
    carousel.addEventListener('mouseleave', startGalleryAutoplay);
  }
  const prevBtn = document.getElementById('galleryPrev');
  const nextBtn = document.getElementById('galleryNext');
  if (prevBtn) prevBtn.addEventListener('click', () => changeGallery(-1));
  if (nextBtn) nextBtn.addEventListener('click', () => changeGallery(1));
});
