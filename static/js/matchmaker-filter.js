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
  const noSavedMsg = document.getElementById('no-saved-msg');

  const updateNoSavedMessage = () => {
    if (!noSavedMsg || !showSavedBtn) return;
    if (showSavedBtn.dataset.mode === 'saved') {
      const any = document.querySelectorAll('.matchmaker-card.bookmarked').length > 0;
      noSavedMsg.classList.toggle('d-none', any);
    } else {
      noSavedMsg.classList.add('d-none');
    }
  };

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
      updateNoSavedMessage();
    });
  }

  document.querySelectorAll('.bookmark-btn').forEach(btn => {
    btn.addEventListener('click', async () => {
      const card = btn.closest('.matchmaker-card');
      const icon = btn.querySelector('i');
      const url = btn.dataset.url;
      if (!card || !icon || !url) return;
      const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]')?.value;
      const isBookmarked = card.classList.contains('bookmarked');
      try {
        const res = await fetch(url, {
          method: 'POST',
          headers: { 'X-CSRFToken': csrftoken },
          body: new URLSearchParams({
            competidor_id: card.dataset.id,
            action: isBookmarked ? 'remove' : 'add',
          }),
        });
        if (res.ok) {
          icon.classList.toggle('bi-bookmark');
          icon.classList.toggle('bi-bookmark-fill');
          card.classList.toggle('bookmarked');
          if (
            showSavedBtn &&
            showSavedBtn.dataset.mode === 'saved' &&
            !card.classList.contains('bookmarked')
          ) {
            const col = card.closest('.col');
            if (col) col.style.display = 'none';
          }
          updateNoSavedMessage();
        }
      } catch (err) {
        console.error(err);
      }
    });
  });

  updateNoSavedMessage();
});

