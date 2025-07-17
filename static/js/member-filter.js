document.addEventListener('DOMContentLoaded', () => {
  const form = document.getElementById('member-filter-form');
  if (!form) return;
  const submit = () => form.requestSubmit ? form.requestSubmit() : form.submit();
  form.querySelectorAll('input, select').forEach(el => {
    el.addEventListener('change', submit);
  });
});
