document.addEventListener('DOMContentLoaded', () => {
  const steps = ['step1', 'step2', 'step3'].map(id => document.getElementById(id));
  const currentInput = document.getElementById('current-step');
  let current = parseInt(currentInput.value, 10) || 1;

  function showStep(n) {
    steps.forEach((step, idx) => {
      if (!step) return;
      step.classList.toggle('d-none', idx !== n - 1);
    });
    current = n;
    currentInput.value = current;
  }

  const next1 = document.getElementById('next1');
  const next2 = document.getElementById('next2');
  const prev2 = document.getElementById('prev2');
  const prev3 = document.getElementById('prev3');

  if (next1) next1.addEventListener('click', () => showStep(2));
  if (next2) next2.addEventListener('click', () => showStep(3));
  if (prev2) prev2.addEventListener('click', () => showStep(1));
  if (prev3) prev3.addEventListener('click', () => showStep(2));

  showStep(current);
});

