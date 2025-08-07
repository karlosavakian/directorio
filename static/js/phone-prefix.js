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

    input.value = '+' + iti.getSelectedCountryData().dialCode;

    // Keep value in sync when the selected country changes
    input.addEventListener('countrychange', function () {
      input.value = '+' + iti.getSelectedCountryData().dialCode;
    });

    // Open the country dropdown when the input itself is clicked
    input.addEventListener('click', function () {
      const flag = input.parentNode.querySelector('.iti__selected-flag');
      if (flag) {
        flag.click();
      }
    });

    // Prevent manual text editing while allowing dropdown interaction
    input.addEventListener('keydown', function (e) {
      e.preventDefault();
    });
  });
});
