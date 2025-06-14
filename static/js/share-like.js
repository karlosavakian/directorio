document.addEventListener('DOMContentLoaded', () => {
  const heart = document.getElementById('club-heart');
  if (heart) {
    heart.addEventListener('click', () => {
      heart.classList.toggle('liked');
    });
  }

  const shareBtn = document.getElementById('club-share');
  if (shareBtn) {
    shareBtn.addEventListener('click', async () => {
      const url = window.location.href;
      if (navigator.share) {
        try {
          await navigator.share({ url });
        } catch (err) {
          console.error(err);
        }
      } else if (navigator.clipboard) {
        try {
          await navigator.clipboard.writeText(url);
          alert('Enlace copiado al portapapeles');
        } catch (err) {
          prompt('Copia este enlace:', url);
        }
      } else {
        prompt('Copia este enlace:', url);
      }
    });
  }
});
