document.addEventListener('DOMContentLoaded', () => {
  const inputs = document.querySelectorAll('input[name="username"], input[id="id_username"]');
  inputs.forEach(input => {
    const wrapper = input.closest('.form-field');
    const statusIcon = wrapper ? wrapper.querySelector('.status-icon') : null;
    if (!statusIcon) return;
    let timer;
    input.addEventListener('input', () => {
      const username = input.value.trim();
      clearTimeout(timer);
      statusIcon.classList.add('d-none');
      statusIcon.classList.remove('bi-check-circle', 'text-success', 'bi-x-circle', 'text-danger');
      if (!username) return;
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
