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
    });
  });
});
