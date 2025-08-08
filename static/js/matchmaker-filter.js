document.addEventListener('DOMContentLoaded', () => {
  const form = document.getElementById('matchmaker-filter-form');
  if (!form) return;

  const clearBtn = document.getElementById('clear-matchmaker-filter-btn');
  if (clearBtn) {
    clearBtn.addEventListener('click', () => {
      form.reset();
      form.querySelectorAll('input[name="mm_sexo"]').forEach(r => (r.checked = false));
      const citySelect = form.querySelector('select[name="mm_ciudad"]');
      if (citySelect) citySelect.value = '';
      const pesoMin = form.querySelector('input[name="mm_peso_min"]');
      const pesoMax = form.querySelector('input[name="mm_peso_max"]');
      if (pesoMin && pesoMax) {
        pesoMin.value = 30;
        pesoMax.value = 160;
      }
      const edadMin = form.querySelector('input[name="mm_edad_min"]');
      const edadMax = form.querySelector('input[name="mm_edad_max"]');
      if (edadMin && edadMax) {
        edadMin.value = 10;
        edadMax.value = 60;
      }
      form.querySelectorAll('.range-slider input[type="range"]').forEach(input => {
        input.dispatchEvent(new Event('input'));
      });
    });
  }

  document.querySelectorAll('.bookmark-btn').forEach(btn => {
    btn.addEventListener('click', () => {
      const icon = btn.querySelector('i');
      if (!icon) return;
      icon.classList.toggle('bi-bookmark');
      icon.classList.toggle('bi-bookmark-fill');
    });
  });
});

