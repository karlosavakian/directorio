document.addEventListener('DOMContentLoaded', () => {
  const form = document.getElementById('matchmaker-filter-form');
  if (!form) return;

  const clearBtn = document.getElementById('clear-matchmaker-filter-btn');
  if (clearBtn) {
    clearBtn.addEventListener('click', () => {
      form.reset();
      form.querySelectorAll('input[name="mm_sexo"]').forEach(r => (r.checked = false));
      const allRadio = form.querySelector('#mm-sexo-all');
      if (allRadio) allRadio.checked = true;
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

  const showSavedBtn = document.getElementById('show-saved');
  const cards = document.querySelectorAll('.matchmaker-card');

  if (showSavedBtn) {
    showSavedBtn.dataset.mode = 'all';
    showSavedBtn.addEventListener('click', () => {
      const showingSaved = showSavedBtn.dataset.mode === 'saved';
      if (showingSaved) {
        cards.forEach(card => {
          const col = card.closest('.col');
          if (col) col.style.display = '';
        });
        showSavedBtn.dataset.mode = 'all';
        showSavedBtn.textContent = 'Mostrar guardados';
        showSavedBtn.classList.add('text-secondary');
        showSavedBtn.classList.remove('text-black');
      } else {
        cards.forEach(card => {
          const col = card.closest('.col');
          if (col) {
            col.style.display = card.classList.contains('bookmarked') ? '' : 'none';
          }
        });
        showSavedBtn.dataset.mode = 'saved';
        showSavedBtn.textContent = 'Mostrar todos';
        showSavedBtn.classList.add('text-black');
        showSavedBtn.classList.remove('text-secondary');
      }
    });
  }

  document.querySelectorAll('.bookmark-btn').forEach(btn => {
    btn.addEventListener('click', () => {
      const icon = btn.querySelector('i');
      if (!icon) return;
      icon.classList.toggle('bi-bookmark');
      icon.classList.toggle('bi-bookmark-fill');
      const card = btn.closest('.matchmaker-card');
      if (card) {
        card.classList.toggle('bookmarked');
        const showSavedBtn = document.getElementById('show-saved');
        if (
          showSavedBtn &&
          showSavedBtn.dataset.mode === 'saved' &&
          !card.classList.contains('bookmarked')
        ) {
          const col = card.closest('.col');
          if (col) col.style.display = 'none';
        }
      }
    });
  });
});

