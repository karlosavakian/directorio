document.addEventListener('DOMContentLoaded', () => {
  const form = document.getElementById('matchmaker-filter-form');
  if (!form) return;

  const citySelect = form.querySelector('select[name="mm_ciudad"]');
  if (citySelect) {
    citySelect.addEventListener('change', () => {
      form.requestSubmit();
    });
  }

  const clearBtn = document.getElementById('clear-matchmaker-filter-btn');
  if (clearBtn) {
    clearBtn.addEventListener('click', () => {
      window.location.href = window.location.pathname;
    });
  }
});
