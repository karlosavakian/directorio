document.addEventListener('DOMContentLoaded', () => {
  const steps = ['step1', 'step2', 'step3', 'step4', 'step5'].map(id => document.getElementById(id));
  const progress = ['step-label-1', 'step-label-2', 'step-label-3', 'step-label-4', 'step-label-5'].map(id => document.getElementById(id));
  const alerts = ['step1-alert', 'step2-alert', 'step3-alert', 'step4-alert', 'step5-alert'].map(id => document.getElementById(id));
  const currentInput = document.getElementById('current-step');
  let current = parseInt(currentInput.value, 10) || 1;
  const tipoCards = document.querySelectorAll('.tipo-card');
  const planCards = document.querySelectorAll('.plan-card');
  const paymentSection = document.getElementById('payment-section');
  const cardInputs = ['id_card_number', 'id_card_expiry', 'id_card_cvc'].map(id => document.getElementById(id));
  const nextBtn = document.getElementById('nextBtn');
  const prevBtn = document.getElementById('prevBtn');
  const finishBtn = document.getElementById('finishBtn');
  const stripeBtn = document.getElementById('stripe-connect-btn');
  const clubFeaturesSection = document.getElementById('club-features-section');
  const coachFeaturesSection = document.getElementById('coach-features-section');
  const logoTitle = document.getElementById('logo-title');
    const nameField = document.getElementById('name-field');
    const nameInput = document.getElementById('id_name');
    const firstNameInput = document.getElementById('id_nombre');
    const lastNameInput = document.getElementById('id_apellidos');
    const coachesSection = document.getElementById('coaches-section');
    const usernameField = document.getElementById('username-field');
    const nameLabel = document.querySelector('label[for="id_name"]');
    const coachContainer = document.getElementById('coaches-formset');
    const addCoachBtn = document.getElementById('add-coach-btn');
    const totalCoachForms = coachContainer ? coachContainer.querySelector('#id_coaches-TOTAL_FORMS') : null;
    const coachTemplate = document.getElementById('coach-empty-form-template');

    function addCoachForm() {
      if (!coachContainer || !totalCoachForms || !coachTemplate) return;
      const index = parseInt(totalCoachForms.value, 10);
      const newForm = coachTemplate.innerHTML.replace(/__prefix__/g, index);
      const temp = document.createElement('div');
      temp.innerHTML = newForm.trim();
      const formElem = temp.firstElementChild;
      coachContainer.appendChild(formElem);
      totalCoachForms.value = index + 1;
    }

    function removeCoachForm(btn) {
      if (!coachContainer || !totalCoachForms) return;
      const form = btn.closest('.coach-form');
      if (!form) return;
      const forms = coachContainer.querySelectorAll('.coach-form');
      if (forms.length <= 1) return;
      form.remove();
      const updatedForms = coachContainer.querySelectorAll('.coach-form');
      totalCoachForms.value = updatedForms.length;
      updatedForms.forEach((f, idx) => {
        f.querySelectorAll('input').forEach(input => {
          input.name = input.name.replace(/coaches-\d+-/, `coaches-${idx}-`);
          input.id = input.id.replace(/coaches-\d+-/, `coaches-${idx}-`);
        });
        f.querySelectorAll('label').forEach(label => {
          label.htmlFor = label.htmlFor.replace(/coaches-\d+-/, `coaches-${idx}-`);
        });
      });
    }

    if (addCoachBtn) {
      addCoachBtn.addEventListener('click', addCoachForm);
    }

    if (coachContainer) {
      coachContainer.addEventListener('click', e => {
        const btn = e.target.closest('.remove-coach-btn');
        if (btn) {
          removeCoachForm(btn);
        }
      });
    }

  function showStep(n) {
    steps.forEach((step, idx) => {
      if (!step) return;
      if (idx === n - 1) {
        step.classList.remove('d-none');
        step.classList.add('fade-step');
        step.addEventListener('animationend', () => step.classList.remove('fade-step'), { once: true });
      } else {
        step.classList.add('d-none');
      }
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
    updateFeatureForms();
  }

  function validateStep(n) {
    const step = steps[n - 1];
    const alert = alerts[n - 1];
    if (alert) alert.classList.add('d-none');
    if (!step) return true;
    const fields = step.querySelectorAll('input, select, textarea');
    fields.forEach(field => {
      const label = step.querySelector(`label[for="${field.id}"]`);
      if (label) {
        const asterisk = label.querySelector('.required-asterisk');
        if (asterisk) asterisk.remove();
      }
      const container = field.closest('.form-field') || field.parentElement;
      if (container) {
        const warn = container.querySelector('.field-required-alert');
        if (warn) warn.remove();
      }
    });
    let firstInvalid = null;
    for (const field of fields) {
      if (field.type === 'radio') {
        const group = step.querySelectorAll(`input[name="${field.name}"]`);
        if (![...group].some(r => r.checked)) {
          if (alert) alert.classList.remove('d-none');
          group.forEach(radio => {
            const lbl = step.querySelector(`label[for="${radio.id}"]`);
            if (lbl && !lbl.querySelector('.required-asterisk')) {
              const span = document.createElement('span');
              span.className = 'text-danger ms-1 required-asterisk';
              span.textContent = '*';
              lbl.appendChild(span);
            }
          });
          firstInvalid = group[0];
          break;
        }
        continue;
      }
      if (field.hasAttribute('required') && !field.value.trim()) {
        if (alert) alert.classList.remove('d-none');
        const label = step.querySelector(`label[for="${field.id}"]`);
        if (label && !label.querySelector('.required-asterisk')) {
          const span = document.createElement('span');
          span.className = 'text-danger ms-1 required-asterisk';
          span.textContent = '*';
          label.appendChild(span);
        }
        const container = field.closest('.form-field') || field.parentElement;
        if (container && !container.querySelector('.field-required-alert')) {
          const div = document.createElement('div');
          div.className = 'field-required-alert text-danger small mt-1';
          div.textContent = 'Este campo es obligatorio.';
          container.appendChild(div);
        }
        if (!firstInvalid) firstInvalid = field;
        continue;
      }
      if (!field.checkValidity()) {
        if (alert) alert.classList.remove('d-none');
        if (!firstInvalid) firstInvalid = field;
      }
    }
    if (firstInvalid) {
      firstInvalid.reportValidity();
      return false;
    }
    return true;
  }

  if (nextBtn) {
    nextBtn.addEventListener('click', () => {
      if (validateStep(current)) {
        showStep(Math.min(current + 1, steps.length));
      }
    });
  }

  if (prevBtn) {
    prevBtn.addEventListener('click', () => showStep(Math.max(current - 1, 1)));
  }

  if (stripeBtn && window.stripePublicKey) {
    const stripe = Stripe(window.stripePublicKey);
    stripeBtn.addEventListener('click', () => {
      fetch('/create-checkout-session/', { method: 'POST' })
        .then(response => response.json())
        .then(data => {
          if (data.sessionId) {
            stripe.redirectToCheckout({ sessionId: data.sessionId });
          }
        });
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
      updateFeatureForms();
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
    const needsPayment = selected && (selected.value === 'plata' || selected.value === 'oro');
    if (paymentSection) {
      paymentSection.classList.toggle('d-none', !needsPayment);
    }
    cardInputs.forEach(input => {
      if (!input) return;
      if (needsPayment) {
        input.setAttribute('required', 'required');
      } else {
        input.removeAttribute('required');
      }
    });
  }

  togglePaymentSection();
  showStep(current);
  updateFeatureForms();

    function updateFeatureForms() {
    const selected = document.querySelector('input[name="tipo"]:checked');
    const value = selected ? selected.value : null;

    if (value === 'club') {
      if (clubFeaturesSection) clubFeaturesSection.classList.remove('d-none');
      if (coachFeaturesSection) coachFeaturesSection.classList.add('d-none');
      if (logoTitle) logoTitle.textContent = 'Logotipo';
      if (nameField) nameField.classList.remove('d-none');
      if (nameInput) {
        nameInput.value = '';
        nameInput.setAttribute('required', 'required');
      }
      if (coachesSection) coachesSection.classList.remove('d-none');
      if (usernameField) {
        usernameField.classList.remove('col-md-12');
        usernameField.classList.add('col-md-6');
      }
      if (nameLabel) nameLabel.textContent = 'Nombre del club';
      if (coachContainer && totalCoachForms) {
        coachContainer.querySelectorAll('.coach-form').forEach(form => form.remove());
        totalCoachForms.value = 0;
        addCoachForm();
      }
    } else if (value === 'entrenador') {
      if (coachFeaturesSection) coachFeaturesSection.classList.remove('d-none');
      if (clubFeaturesSection) clubFeaturesSection.classList.add('d-none');
      if (logoTitle) logoTitle.textContent = 'Foto de perfil';
      if (nameField) nameField.classList.add('d-none');
      if (nameInput) {
        const first = firstNameInput ? firstNameInput.value.trim() : '';
        const last = lastNameInput ? lastNameInput.value.trim() : '';
        nameInput.value = `${first} ${last}`.trim();
        nameInput.removeAttribute('required');
      }
      if (usernameField) {
        usernameField.classList.remove('col-md-6');
        usernameField.classList.add('col-md-12');
      }
      if (nameLabel) nameLabel.textContent = 'Nombre';
      if (coachesSection) {
        coachesSection.classList.add('d-none');
        coachesSection.querySelectorAll('input').forEach(input => {
          input.removeAttribute('required');
        });
        if (coachContainer) coachContainer.querySelectorAll('.coach-form').forEach(f => f.remove());
        if (totalCoachForms) totalCoachForms.value = 0;
      }
    } else {
      if (clubFeaturesSection) clubFeaturesSection.classList.add('d-none');
      if (coachFeaturesSection) coachFeaturesSection.classList.add('d-none');
      if (usernameField) {
        usernameField.classList.remove('col-md-12');
        usernameField.classList.add('col-md-6');
      }
      if (nameLabel) nameLabel.textContent = 'Nombre';
    }
  }
});

