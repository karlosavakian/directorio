document.addEventListener('DOMContentLoaded', () => {
  document.querySelectorAll('.post-like').forEach(btn => {
    btn.addEventListener('click', async () => {
      const url = btn.dataset.url;
      const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]')?.value;
      const countSpan = btn.querySelector('.like-count');

      btn.classList.toggle('liked');

      try {
        const res = await fetch(url, {
          method: 'POST',
          headers: {
            'X-CSRFToken': csrftoken,
            'X-Requested-With': 'XMLHttpRequest'
          },
          credentials: 'same-origin'
        });
        if (res.redirected) {
          const modal = document.getElementById('loginModal');
          if (modal) new bootstrap.Modal(modal).show();
          btn.classList.toggle('liked');
          return;
        }
        if (res.ok) {
          const data = await res.json();
          btn.classList.toggle('liked', data.liked);
          if (countSpan) countSpan.textContent = data.count;
        } else {
          btn.classList.toggle('liked');
        }
      } catch (err) {
        console.error(err);
        btn.classList.toggle('liked');
      }
    });
  });
});
