// Initialize intl-tel-input for prefix fields and format phone inputs
document.addEventListener('DOMContentLoaded', function () {
  const inputs = document.querySelectorAll('input.prefijo-input');
  inputs.forEach(function (input) {
    const iti = window.intlTelInput(input, {
      initialCountry: 'es',
      separateDialCode: true,
      utilsScript: 'https://cdn.jsdelivr.net/npm/intl-tel-input@17.0.19/build/js/utils.js'
    });

    // Hide the input so only the dropdown is visible
    input.style.display = 'none';

    // Set initial value for form submission
    input.value = '+' + iti.getSelectedCountryData().dialCode;

    // Keep value in sync when the selected country changes
    input.addEventListener('countrychange', function () {
      input.value = '+' + iti.getSelectedCountryData().dialCode;
    });
  });

  // Format phone fields as xxx.xx.xx.xx
  const phoneInputs = document.querySelectorAll('input.telefono-input');
  phoneInputs.forEach(function (input) {
    input.addEventListener('input', function () {
      const digits = input.value.replace(/\D/g, '').substring(0, 9);
      let formatted = '';
      if (digits.length > 0) {
        formatted = digits.substring(0, 3);
      }
      if (digits.length >= 4) {
        formatted += '.' + digits.substring(3, 5);
      }
      if (digits.length >= 6) {
        formatted += '.' + digits.substring(5, 7);
      }
      if (digits.length >= 8) {
        formatted += '.' + digits.substring(7, 9);
      }
      input.value = formatted;
    });
  });
});
