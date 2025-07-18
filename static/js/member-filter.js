document.addEventListener('DOMContentLoaded', () => {
  // Previously the form submitted automatically on input change.
  // Se deshabilita el auto envío para que el filtrado solo ocurra
  // al presionar el botón correspondiente.
  const form = document.getElementById('member-filter-form');
  if (!form) return;
  // No listeners: el usuario debe pulsar "Filtrar".

  const clearBtn = document.getElementById('clear-filter-btn');
  if (clearBtn) {
    clearBtn.addEventListener('click', () => {
      window.location.href = window.location.pathname;
    });
  }
});
