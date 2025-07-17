document.addEventListener('DOMContentLoaded', () => {
  const form = document.getElementById('member-filter-form');
  if (!form) return;
  form.querySelectorAll('input, select').forEach(el => {
    el.addEventListener('change', () => {
      form.submit();
    });
  });
});
