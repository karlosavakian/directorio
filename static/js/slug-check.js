document.addEventListener('DOMContentLoaded', () => {
  const input = document.getElementById('id_slug');
  const status = document.getElementById('slug-status');
  const error = document.getElementById('slug-error');
  if (!input || !status) return;
  const current = input.dataset.current || '';

  const showError = (msg) => {
    status.innerHTML = '<i class="bi bi-x-circle text-danger"></i>';
    if (error) {
      error.textContent = msg;
      error.classList.remove('d-none');
    }
  };

  const clearError = () => {
    status.innerHTML = '';
    if (error) {
      error.textContent = '';
      error.classList.add('d-none');
    }
  };

  if (error && error.textContent.trim()) {
    status.innerHTML = '<i class="bi bi-x-circle text-danger"></i>';
  }

  let timer;
  input.addEventListener('input', () => {
    const value = input.value.trim();
    clearTimeout(timer);
    if (!value) {
      clearError();
      return;
    }
    if (value.length < 3) {
      showError('Introduce un nombre con al menos 3 carácteres');
      return;
    }
    clearError();
    timer = setTimeout(() => {
      fetch(`/clubs/slug-disponible/?slug=${encodeURIComponent(value)}&current=${encodeURIComponent(current)}`)
        .then(res => res.json())
        .then(data => {
          status.innerHTML = data.available
            ? '<i class="bi bi-check-circle text-success"></i>'
            : '<i class="bi bi-x-circle text-danger"></i>';
        })
        .catch(() => {
          status.innerHTML = '';
        });
    }, 300);
  });

  const form = input.closest('form');
  if (form) {
    form.addEventListener('submit', (e) => {
      const value = input.value.trim();
      if (value.length < 3) {
        e.preventDefault();
        showError('Introduce un nombre con al menos 3 carácteres');
      }
    });
  }
});
