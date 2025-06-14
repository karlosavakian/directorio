document.addEventListener('DOMContentLoaded', function() {
  document.querySelectorAll('.modal').forEach(function(modalEl) {
    modalEl.addEventListener('hidden.bs.modal', function () {
      document.querySelectorAll('.modal-backdrop').forEach(b => b.remove());
      document.body.classList.remove('modal-open');
      document.body.style.removeProperty('padding-right');
    });
  });
});
