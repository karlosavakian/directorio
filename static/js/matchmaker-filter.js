document.addEventListener('DOMContentLoaded', () => {
  const form = document.getElementById('matchmaker-filter-form');
  if (!form) return;

  const clearBtn = document.getElementById('clear-matchmaker-filter-btn');
  if (clearBtn) {
    clearBtn.addEventListener('click', () => {
      window.location.href = window.location.pathname;
    });
  }
});
