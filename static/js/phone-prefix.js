// Initialize intl-tel-input on phone fields
function initPhoneInputs(root = document) {
  const phoneInputs = root.querySelectorAll('input.phone-input');
  phoneInputs.forEach(function (input) {
    if (input.dataset.phoneInitialized) return;
    input.dataset.phoneInitialized = 'true';

    const iti = window.intlTelInput(input, {
      initialCountry: 'es',
      separateDialCode: true,
      utilsScript: 'https://cdn.jsdelivr.net/npm/intl-tel-input@17.0.19/build/js/utils.js'
    });

    const itiContainer = input.closest('.iti');
    const cleanCountryNames = () => {
      itiContainer?.querySelectorAll('.iti__country-name').forEach(el => {
        el.textContent = el.textContent.replace(/\s*\([^)]*\)/, '');
      });
    };
    cleanCountryNames();
    input.addEventListener('open:countrydropdown', cleanCountryNames);

    const prefijoInput = input.closest('.form-field')?.querySelector('input.prefijo-input');
    if (prefijoInput) {
      if (prefijoInput.value) {
        const code = prefijoInput.value.replace('+', '');
        const country = window.intlTelInputGlobals
          .getCountryData()
          .find(c => c.dialCode === code);
        if (country) {
          iti.setCountry(country.iso2);
        }
      }
      prefijoInput.value = '+' + iti.getSelectedCountryData().dialCode;
    }
    input.addEventListener('countrychange', function () {
      if (prefijoInput) {
        prefijoInput.value = '+' + iti.getSelectedCountryData().dialCode;
      }
      input.dispatchEvent(new Event('input', { bubbles: true }));
    });

    const format = () => {
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

    format();
    input.addEventListener('input', format);

    const isValidSpanishPhone = () => {
      const prefijo = input.closest('.form-field')?.querySelector('input.prefijo-input')?.value || '';
      const digits = input.value.replace(/\D/g, '');
      if (prefijo === '+34' && digits && !['6', '7', '9'].includes(digits.charAt(0))) {
        alert('Introduce un número de teléfono válido');
        return false;
      }
      return true;
    };

    input.form?.addEventListener('submit', function (e) {
      if (!isValidSpanishPhone()) {
        e.preventDefault();
      }
    });
  });
}

document.addEventListener('DOMContentLoaded', function () {
  initPhoneInputs();
});

window.initPhoneInputs = initPhoneInputs;
