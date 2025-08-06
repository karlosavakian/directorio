document.addEventListener('DOMContentLoaded', () => {
  const input = document.getElementById('id_slug');
  const status = document.getElementById('slug-status');
  if (!input || !status) return;
  const current = input.dataset.current || '';
  let timer;
  input.addEventListener('input', () => {
    const value = input.value.trim();
    clearTimeout(timer);
    if (!value) {
      status.innerHTML = '';
      status.classList.remove('text-danger');
      return;
    }
    if (value.length < 3) {
      status.textContent = 'Introduce un nombre con al menos 3 carácteres';
      status.classList.add('text-danger');
      return;
    }
    status.classList.remove('text-danger');
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
});
