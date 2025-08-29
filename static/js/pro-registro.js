document.addEventListener('DOMContentLoaded', () => {
  const steps = ['step1', 'step2', 'step3', 'step4'].map(id => document.getElementById(id));
  const progress = ['step-label-1', 'step-label-2', 'step-label-3', 'step-label-4'].map(id => document.getElementById(id));
  const alerts = ['step1-alert', null, 'step3-alert', 'step4-alert'].map(id => id ? document.getElementById(id) : null);
  const step4Alert = alerts[3];
  const currentInput = document.getElementById('current-step');
  let current = parseInt(currentInput.value, 10) || 1;
  const tipoCards = document.querySelectorAll('.tipo-card');
  const planCards = document.querySelectorAll('.plan-card');
  const nextBtn = document.getElementById('nextBtn');
  const prevBtn = document.getElementById('prevBtn');
  const finishBtn = document.getElementById('finishBtn');
  const paymentForm = document.getElementById('payment-form');
  const cardErrors = document.getElementById('card-errors');
  const submitPaymentBtn = document.getElementById('submit-payment');
  let cardElement = null;
  let paymentCompleted = false;
  let requiresPayment = false;
  const clubFeaturesSection = document.getElementById('club-features-section');
  const coachFeaturesSection = document.getElementById('coach-features-section');
  const logoTitle = document.getElementById('logo-title');
  const step4Elem = document.getElementById('step4');
  const stepLabel4 = document.getElementById('step-label-4');
  let maxStep = step4Elem ? 4 : 3;
    const nameField = document.getElementById('name-field');
    const nameInput = document.getElementById('id_name');
    const firstNameInput = document.getElementById('id_nombre');
    const lastNameInput = document.getElementById('id_apellidos');
    const coachesSection = document.getElementById('coaches-section');
    const usernameField = document.getElementById('username-field');
    const nameLabel = document.querySelector('label[for="id_name"]');
    const coachContainer = document.getElementById('coaches-formset');
    const addCoachBtn = document.getElementById('add-coach-btn');
    const removeCoachBtn = document.getElementById('remove-coach-btn');
    const totalCoachForms = coachContainer ? coachContainer.querySelector('#id_coaches-TOTAL_FORMS') : null;
    const coachTemplate = document.getElementById('coach-empty-form-template');

    function addCoachForm() {
      if (!coachContainer || !totalCoachForms || !coachTemplate) return;
      const index = parseInt(totalCoachForms.value, 10);
      const newForm = coachTemplate.innerHTML.replace(/__prefix__/g, index);
      const temp = document.createElement('div');
      temp.innerHTML = newForm.trim();
      const formElem = temp.firstElementChild;
      formElem.querySelectorAll('input').forEach(input => {
        input.setAttribute('required', 'required');
      });
      coachContainer.appendChild(formElem);
      totalCoachForms.value = index + 1;
    }

    function removeLastCoachForm() {
      if (!coachContainer || !totalCoachForms) return;
      const forms = coachContainer.querySelectorAll('.coach-form');
      if (forms.length <= 1) return;
      forms[forms.length - 1].remove();
      totalCoachForms.value = forms.length - 1;
    }

    if (addCoachBtn) {
      addCoachBtn.addEventListener('click', addCoachForm);
    }

    if (removeCoachBtn) {
      removeCoachBtn.addEventListener('click', removeLastCoachForm);
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
      item.classList.toggle('active', idx <= n - 1 && idx < maxStep);
    });
    current = n;
    currentInput.value = current;
    if (prevBtn) prevBtn.classList.toggle('d-none', n === 1);
    if (nextBtn) nextBtn.classList.toggle('d-none', n === maxStep);
    if (finishBtn) {
      const hideFinish = n !== maxStep || (requiresPayment && !paymentCompleted);
      finishBtn.classList.toggle('d-none', hideFinish);
      finishBtn.disabled = requiresPayment && !paymentCompleted;
    }
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
      if (field.type === 'hidden' || field.offsetParent === null) {
        continue;
      }
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
        firstInvalid = field;
        break;
      }
      if (!field.checkValidity()) {
        if (alert) alert.classList.remove('d-none');
        firstInvalid = field;
        break;
      }
    }

    let featureInvalid = false;
    if (n === 3) {
      const checkGroup = (section, name) => {
        if (!section || section.classList.contains('d-none')) return;
        const selected = section.querySelectorAll(`input[name="${name}"]:checked`).length;
        let error = section.querySelector('.min-select-alert');
        if (selected < 3) {
          if (!error) {
            error = document.createElement('div');
            error.className = 'invalid-feedback d-block min-select-alert';
            error.textContent = 'Selecciona al menos 3 opciones.';
            section.appendChild(error);
          }
          if (!firstInvalid) {
            const input = section.querySelector(`input[name="${name}"]`);
            if (input) firstInvalid = input;
          }
          featureInvalid = true;
        } else if (error) {
          error.remove();
        }
      };
      checkGroup(clubFeaturesSection, 'features');
      checkGroup(coachFeaturesSection, 'coach_features');
    }

    if (firstInvalid || featureInvalid) {
      if (alert) alert.classList.remove('d-none');
      if (firstInvalid && firstInvalid.offsetParent !== null) firstInvalid.reportValidity();
      return false;
    }
    if (n === maxStep && requiresPayment && !paymentCompleted) {
      if (alert) {
        alert.textContent = 'Completa el pago antes de continuar.';
        alert.classList.remove('d-none');
      }
      return false;
    }
    return true;
  }

  if (nextBtn) {
    nextBtn.addEventListener('click', () => {
      if (validateStep(current)) {
        showStep(Math.min(current + 1, maxStep));
      }
    });
  }

  if (prevBtn) {
    prevBtn.addEventListener('click', () => showStep(Math.max(current - 1, 1)));
  }

  if (finishBtn) {
    finishBtn.addEventListener('click', (e) => {
      if (!validateStep(current)) {
        e.preventDefault();
      }
    });
  }

  if (paymentForm && window.stripePublicKey) {
    const stripe = Stripe(window.stripePublicKey);
    const elements = stripe.elements();
    cardElement = elements.create('card');
    cardElement.mount('#card-element');

    paymentForm.addEventListener('submit', async (e) => {
      e.preventDefault();
      if (cardErrors) {
        cardErrors.textContent = '';
        cardErrors.classList.remove('text-success');
        cardErrors.classList.add('text-danger');
      }
      if (step4Alert) step4Alert.classList.add('d-none');
      if (submitPaymentBtn) {
        submitPaymentBtn.disabled = true;
        submitPaymentBtn.textContent = 'Procesando...';
      }
      try {
        const response = await fetch('/create-payment-intent/', { method: 'POST' });
        const data = await response.json();
        const { error, paymentIntent } = await stripe.confirmCardPayment(data.clientSecret, {
          payment_method: { card: cardElement }
        });
        if (error) {
          if (cardErrors) cardErrors.textContent = error.message || 'Error al procesar el pago.';
          if (step4Alert) {
            step4Alert.textContent = 'Se produjo un error al procesar la tarjeta.';
            step4Alert.classList.remove('d-none');
          }
          if (submitPaymentBtn) {
            submitPaymentBtn.disabled = false;
            submitPaymentBtn.textContent = 'Pagar';
          }
        } else if (paymentIntent && paymentIntent.status === 'succeeded') {
          paymentCompleted = true;
          if (cardErrors) {
            cardErrors.classList.remove('text-danger');
            cardErrors.classList.add('text-success');
            cardErrors.textContent = 'Pago realizado con éxito.';
          }
          if (submitPaymentBtn) {
            submitPaymentBtn.classList.add('d-none');
            submitPaymentBtn.disabled = false;
            submitPaymentBtn.textContent = 'Pagar';
          }
          showStep(maxStep);
        }
      } catch (err) {
        if (cardErrors) cardErrors.textContent = 'Error al procesar el pago.';
        if (step4Alert) {
          step4Alert.textContent = 'Se produjo un error al procesar la tarjeta.';
          step4Alert.classList.remove('d-none');
        }
        if (submitPaymentBtn) {
          submitPaymentBtn.disabled = false;
          submitPaymentBtn.textContent = 'Pagar';
        }
      }
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
      togglePaymentStep();
    });
  });

  function togglePaymentStep() {
    const selected = document.querySelector('input[name="plan"]:checked');
    requiresPayment = !!(selected && selected.value !== 'bronce' && paymentForm);
    paymentCompleted = false;
    if (step4Elem) step4Elem.classList.toggle('d-none', !requiresPayment);
    if (stepLabel4) stepLabel4.classList.toggle('d-none', !requiresPayment);
    maxStep = requiresPayment ? 4 : 3;
    if (finishBtn) finishBtn.disabled = requiresPayment;
    if (submitPaymentBtn) {
      submitPaymentBtn.classList.toggle('d-none', !requiresPayment);
      submitPaymentBtn.disabled = false;
      submitPaymentBtn.textContent = 'Pagar';
    }
    if (current > maxStep) current = maxStep;
    showStep(current);
  }

  togglePaymentStep();
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

