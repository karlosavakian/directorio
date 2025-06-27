document.addEventListener('DOMContentLoaded', () => {
  document.querySelectorAll('select[name="estado"]').forEach(select => {
    const row = select.closest('.row');
    if (!row) return;
    const startCol = row.querySelector('input[name="hora_inicio"]').closest('.col');
    const endCol = row.querySelector('input[name="hora_fin"]').closest('.col');
    function toggleFields() {
      const abierto = select.value === 'abierto';
      startCol.style.display = abierto ? '' : 'none';
      endCol.style.display = abierto ? '' : 'none';
      if (!abierto) {
        const startInput = startCol.querySelector('input[name="hora_inicio"]');
        const endInput = endCol.querySelector('input[name="hora_fin"]');
        if (!startInput.value) startInput.value = '00:00';
        if (!endInput.value) endInput.value = '00:00';
      }
    }
    select.addEventListener('change', toggleFields);
    toggleFields();
  });
});
