document.addEventListener('DOMContentLoaded', () => {
  const steps = ['step1', 'step2', 'step3'].map(id => document.getElementById(id));
  const progress = ['step-label-1', 'step-label-2', 'step-label-3'].map(id => document.getElementById(id));
  const currentInput = document.getElementById('current-step');
  let current = parseInt(currentInput.value, 10) || 1;
  const clubFields = document.getElementById('club-fields');
  const coachFields = document.getElementById('coach-fields');
  const tipoRadios = document.querySelectorAll('input[name="tipo"]');
  const planCards = document.querySelectorAll('.plan-card');

  function showStep(n) {
    steps.forEach((step, idx) => {
      if (!step) return;
      step.classList.toggle('d-none', idx !== n - 1);
    });
    progress.forEach((item, idx) => {
      if (!item) return;
      item.classList.toggle('active', idx === n - 1);
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

  function toggleTipoFields() {
    const checked = document.querySelector('input[name="tipo"]:checked');
    if (!checked) return;
    if (checked.value === 'club') {
      clubFields && clubFields.classList.remove('d-none');
      coachFields && coachFields.classList.add('d-none');
    } else if (checked.value === 'entrenador') {
      coachFields && coachFields.classList.remove('d-none');
      clubFields && clubFields.classList.add('d-none');
    } else {
      clubFields && clubFields.classList.add('d-none');
      coachFields && coachFields.classList.add('d-none');
    }
  }

  tipoRadios.forEach(radio => radio.addEventListener('change', toggleTipoFields));

  planCards.forEach(card => {
    const input = card.querySelector('input');
    card.addEventListener('click', () => {
      input.checked = true;
      planCards.forEach(c => c.classList.toggle('active', c === card));
    });
  });

  toggleTipoFields();

  showStep(current);
});

