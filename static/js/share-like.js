document.addEventListener('DOMContentLoaded', () => {
  const heart = document.getElementById('club-heart');
  if (heart) {
    heart.addEventListener('click', async () => {
      const url = heart.dataset.url;
      const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;
      try {
        const res = await fetch(url, {
          method: 'POST',
          headers: { 'X-CSRFToken': csrftoken },
          credentials: 'same-origin'
        });
        if (res.ok) {
          heart.classList.toggle('liked');
        }
      } catch (err) {
        console.error(err);
      }
    });
  }
});