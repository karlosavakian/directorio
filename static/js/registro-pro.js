document.addEventListener('DOMContentLoaded', () => {
  const steps = document.querySelectorAll('#registro-pro-form .step');
  let current = 0;

  function update() {
    steps.forEach((step, i) => {
      step.style.display = i === current ? '' : 'none';
    });
  }

  document.querySelectorAll('#registro-pro-form .next-btn').forEach(btn => {
    btn.addEventListener('click', () => {
      if (current < steps.length - 1) {
        current += 1;
        update();
      }
    });
  });

  document.querySelectorAll('#registro-pro-form .back-btn').forEach(btn => {
    btn.addEventListener('click', () => {
      if (current > 0) {
        current -= 1;
        update();
      }
    });
  });

  update();
});
