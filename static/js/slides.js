let current = 0;
let autoplayTimer = null;

const slides = document.querySelectorAll(".review-slide");
const prevBtn = document.getElementById("prevBtn");
const nextBtn = document.getElementById("nextBtn");

function updateSlides() {
  slides.forEach((slide, index) => {
    slide.classList.toggle("active", index === current);
  });

  prevBtn.style.display = current > 0 ? "block" : "none";
  nextBtn.style.display = current < slides.length - 1 ? "block" : "none";
}

function changeSlide(direction) {
  current = (current + direction + slides.length) % slides.length;
  updateSlides();
}

function startAutoplay() {
  autoplayTimer = setInterval(() => {
    current = (current + 1) % slides.length;
    updateSlides();
  }, 5000);
}

function pauseAutoplay() {
  clearInterval(autoplayTimer);
}

document.addEventListener("DOMContentLoaded", () => {
  updateSlides();
  startAutoplay();
});
