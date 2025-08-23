document.addEventListener('DOMContentLoaded', () => {
  const steps = ['step1', 'step2', 'step3', 'step4', 'step5'].map(id => document.getElementById(id));
  const progress = ['step-label-1', 'step-label-2', 'step-label-3', 'step-label-4', 'step-label-5'].map(id => document.getElementById(id));
  const currentInput = document.getElementById('current-step');
  let current = parseInt(currentInput.value, 10) || 1;
  const tipoCards = document.querySelectorAll('.tipo-card');
  const planCards = document.querySelectorAll('.plan-card');
  const paymentSection = document.getElementById('payment-section');
  const nextBtn = document.getElementById('nextBtn');
  const prevBtn = document.getElementById('prevBtn');
  const finishBtn = document.getElementById('finishBtn');
  const stripeBtn = document.getElementById('stripe-connect-btn');

  function showStep(n) {
    steps.forEach((step, idx) => {
      if (!step) return;
      step.classList.toggle('active', idx === n - 1);
    });
    progress.forEach((item, idx) => {
      if (!item) return;
      item.classList.toggle('active', idx <= n - 1);
    });
    current = n;
    currentInput.value = current;
    if (prevBtn) prevBtn.classList.toggle('d-none', n === 1);
    if (nextBtn) nextBtn.classList.toggle('d-none', n === steps.length);
    if (finishBtn) finishBtn.classList.toggle('d-none', n !== steps.length);
  }

  if (nextBtn) {
    nextBtn.addEventListener('click', () => showStep(Math.min(current + 1, steps.length)));
  }

  if (prevBtn) {
    prevBtn.addEventListener('click', () => showStep(Math.max(current - 1, 1)));
  }

  if (stripeBtn && window.stripePublicKey) {
    const stripe = Stripe(window.stripePublicKey);
    stripeBtn.addEventListener('click', () => {
      // Placeholder para el flujo de Stripe Connect en modo prueba
      console.log('Stripe Connect init in test mode');
    });
  }

  tipoCards.forEach(card => {
    const input = card.querySelector('input');
    if (input.checked) {
      card.classList.add('active');
    }
    card.addEventListener('click', () => {
      input.checked = true;
      tipoCards.forEach(c => c.classList.toggle('active', c === card));
    });
  });

  planCards.forEach(card => {
    const input = card.querySelector('input');
    if (input.checked) {
      card.classList.add('active');
    }
    card.addEventListener('click', () => {
      input.checked = true;
      planCards.forEach(c => c.classList.toggle('active', c === card));
      togglePaymentSection();
    });
  });

  function togglePaymentSection() {
    const selected = document.querySelector('input[name="plan"]:checked');
    if (selected && (selected.value === 'plata' || selected.value === 'oro')) {
      paymentSection && paymentSection.classList.remove('d-none');
    } else {
      paymentSection && paymentSection.classList.add('d-none');
    }
  }

  togglePaymentSection();

  showStep(current);
});

