document.addEventListener('DOMContentLoaded', () => {
  const inputs = document.querySelectorAll('input[name*="username"], input[id*="username"]');
  inputs.forEach(input => {
    const wrapper = input.closest('.form-field') || input.parentElement;
    let statusIcon = wrapper.querySelector('.status-icon');
    if (!statusIcon) {
      statusIcon = document.createElement('i');
      statusIcon.className = 'status-icon bi d-none';
      wrapper.appendChild(statusIcon);
    }
    let timer;
    input.addEventListener('input', () => {
      const username = input.value.trim();
      clearTimeout(timer);
      statusIcon.classList.add('d-none');
      statusIcon.classList.remove('bi-check-circle', 'text-success', 'bi-x-circle', 'text-danger');
      if (!username) return;
      const pattern = /^[A-Za-z0-9_-]{3,}$/;
      if (!pattern.test(username)) {
        statusIcon.classList.remove('d-none');
        statusIcon.classList.add('bi-x-circle', 'text-danger');
        return;
      }
      timer = setTimeout(() => {
        fetch(`/users/check-username/?username=${encodeURIComponent(username)}`)
          .then(res => res.json())
          .then(data => {
            statusIcon.classList.remove('d-none');
            if (data.available) {
              statusIcon.classList.add('bi-check-circle', 'text-success');
            } else {
              statusIcon.classList.add('bi-x-circle', 'text-danger');
            }
          })
          .catch(() => {});
      }, 300);
    });
  });
});
