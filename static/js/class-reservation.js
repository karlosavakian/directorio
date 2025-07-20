document.addEventListener('DOMContentLoaded', function () {
    const select = document.getElementById('id_class_type');
    const dateField = document.getElementById('reservation-date-field');
    const dateInput = document.getElementById('id_date');
    const submitBtn = document.getElementById('reservation-submit');

    function toggleDate() {
        if (select.value) {
            dateField.style.display = 'block';
        } else {
            dateField.style.display = 'none';
            submitBtn.style.display = 'none';
            dateInput.value = '';
        }
    }

    function toggleSubmit() {
        if (dateInput.value) {
            submitBtn.style.display = 'block';
        } else {
            submitBtn.style.display = 'none';
        }
    }

    if (select) {
        toggleDate();
        select.addEventListener('change', toggleDate);
    }
    if (dateInput) {
        dateInput.addEventListener('change', toggleSubmit);
    }
});
