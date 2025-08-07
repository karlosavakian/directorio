// Initialize intl-tel-input for prefix fields
// Applies to inputs with class 'prefijo-input'
document.addEventListener('DOMContentLoaded', function () {
  const inputs = document.querySelectorAll('input.prefijo-input');
  inputs.forEach(function (input) {
    const iti = window.intlTelInput(input, {
      initialCountry: 'es',
      separateDialCode: true,
      utilsScript: 'https://cdn.jsdelivr.net/npm/intl-tel-input@17.0.19/build/js/utils.js'
    });
    input.setAttribute('readonly', true);
    input.value = '+' + iti.getSelectedCountryData().dialCode;
    input.addEventListener('countrychange', function () {
      input.value = '+' + iti.getSelectedCountryData().dialCode;
      const phoneInput = input.closest('.form-field').querySelector('input.phone-input');
      if (phoneInput) {
        phoneInput.dispatchEvent(new Event('input', { bubbles: true }));
      }
    });
  });

  const phoneInputs = document.querySelectorAll('input.phone-input');
  const format = (input) => {
    const prefijo = input.closest('.form-field')?.querySelector('input.prefijo-input')?.value || '';
    let digits = input.value.replace(/\D/g, '');
    if (prefijo === '+34') {
      digits = digits.slice(0, 9);
    } else {
      digits = digits.slice(0, 15);
    }
    const parts = [];
    if (digits.length > 0) parts.push(digits.slice(0, 3));
    if (digits.length >= 4) parts.push(digits.slice(3, 5));
    if (digits.length >= 6) parts.push(digits.slice(5, 7));
    if (digits.length >= 8) parts.push(digits.slice(7, 9));
    if (digits.length > 9) parts.push(digits.slice(9));
    input.value = parts.filter(Boolean).join(' ').trim();
  };

  phoneInputs.forEach(function (input) {
    format(input);
    input.addEventListener('input', function () {
      format(input);
    });
  });
});
