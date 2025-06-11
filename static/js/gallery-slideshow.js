let galleryIndex = 0;

function showGallerySlide(i) {
  const slides = document.querySelectorAll('.gallery-slide');
  const dots = document.querySelectorAll('.gallery-dot');
  const prev = document.getElementById('galleryPrev');
  const next = document.getElementById('galleryNext');

  if (!slides.length) return;
  galleryIndex = (i + slides.length) % slides.length;
  slides.forEach((s, idx) => {
    s.classList.toggle('active', idx === galleryIndex);
  });
  dots.forEach((d, idx) => {
    d.classList.toggle('active', idx === galleryIndex);
  });
  if (prev && next) {
    prev.style.display = galleryIndex === 0 ? 'none' : 'flex';
    next.style.display = galleryIndex === slides.length - 1 ? 'none' : 'flex';
  }
}

document.addEventListener('DOMContentLoaded', () => {
  const prev = document.getElementById('galleryPrev');
  const next = document.getElementById('galleryNext');
  const dots = document.querySelectorAll('.gallery-dot');
  prev && prev.addEventListener('click', () => showGallerySlide(galleryIndex - 1));
  next && next.addEventListener('click', () => showGallerySlide(galleryIndex + 1));
  dots.forEach((dot, idx) => {
    dot.addEventListener('click', () => showGallerySlide(idx));
  });
  showGallerySlide(0);
});
