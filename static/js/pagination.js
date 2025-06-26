document.addEventListener('click', function(e) {
  const link = e.target.closest('.pagination.ajax a');
  if (!link) return;
  e.preventDefault();
  const pagination = link.closest('.pagination.ajax');
  const targetId = pagination.dataset.target;
  const container = document.getElementById(targetId);
  if (!container) { window.location = link.href; return; }
  fetch(link.href, { headers: { 'X-Requested-With': 'XMLHttpRequest' }})
    .then(res => res.text())
    .then(html => {
      container.classList.add('fade-out');
      setTimeout(() => {
        container.innerHTML = html;
        container.classList.remove('fade-out');
      }, 300);
    })
    .catch(() => { window.location = link.href; });
});
