document.addEventListener('DOMContentLoaded', () => {
  const attachMessageLike = (btn) => {
    const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]')?.value;
    btn._originalParent = btn.parentElement;
    btn._bubble = btn.closest('.message-row')?.querySelector('.message-bubble');

    const moveInside = () => {
      if (!btn._bubble) return;
      btn._bubble.appendChild(btn);
      btn.classList.add('inside', 'animating');
      btn.addEventListener('animationend', () => btn.classList.remove('animating'), { once: true });
    };

    const moveOutside = () => {
      btn._originalParent?.appendChild(btn);
      btn.classList.remove('inside');
    };

    if (btn.classList.contains('liked')) {
      moveInside();
    }

    btn.addEventListener('click', async () => {
      const url = btn.dataset.url;
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
          if (data.liked) {
            moveInside();
          } else {
            moveOutside();
          }
          if (countSpan) countSpan.textContent = data.count;
        } else {
          btn.classList.toggle('liked');
        }
      } catch (err) {
        console.error(err);
        btn.classList.toggle('liked');
      }
    });
  };

  document.querySelectorAll('.message-like').forEach(attachMessageLike);
  window.attachMessageLike = attachMessageLike;
});
