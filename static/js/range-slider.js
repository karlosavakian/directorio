document.addEventListener('DOMContentLoaded', () => {
  document.querySelectorAll('.range-slider').forEach(slider => {
    const inputs = slider.querySelectorAll('input[type="range"]');
    if (inputs.length !== 2) return;
    const [minInput, maxInput] = inputs;
    const minVal = slider.querySelector('.min-value');
    const maxVal = slider.querySelector('.max-value');
    const track = slider.querySelector('.slider-track');

    const update = () => {
      let min = parseInt(minInput.value);
      let max = parseInt(maxInput.value);
      if (min > max) {
        [min, max] = [max, min];
      }
      minInput.value = min;
      maxInput.value = max;
      const range = parseInt(minInput.max) - parseInt(minInput.min);
      const start = ((min - minInput.min) / range) * 100;
      const end = ((max - minInput.min) / range) * 100;
      track.style.left = start + '%';
      track.style.right = (100 - end) + '%';
      if (minVal) minVal.textContent = min;
      if (maxVal) maxVal.textContent = max;
    };

    minInput.addEventListener('input', update);
    maxInput.addEventListener('input', update);
    update();
  });
});
