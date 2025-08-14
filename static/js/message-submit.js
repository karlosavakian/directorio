document.addEventListener('DOMContentLoaded', () => {
  const form = document.getElementById('message-form');
  if (!form) return;

  const container = document.getElementById('message-container');
  const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]')?.value;
  const textarea = form.querySelector('textarea');
  const replyPreview = document.getElementById('reply-preview');
  const replyText = document.getElementById('reply-text');
  const replyClose = document.getElementById('reply-close');

  const clearReplyPreview = () => {
    replyPreview?.classList.add('d-none');
    if (replyText) replyText.textContent = '';
  };
  replyClose?.addEventListener('click', () => {
    clearReplyPreview();
    textarea?.focus();
  });

  const attachReplyHandler = (btn) => {
    btn.addEventListener('click', () => {
      const row = btn.closest('.message-row');
      const text = row?.querySelector('.message-bubble div')?.textContent.trim();
      if (text) {
        if (replyText) replyText.textContent = text;
        replyPreview?.classList.remove('d-none');
        textarea?.focus();
      }
    });
  };

  const scrollToBottom = () => {
    container?.scrollTo({ top: container.scrollHeight });
  };

  scrollToBottom();

  document.querySelectorAll('.reply-btn').forEach(attachReplyHandler);

  if (textarea) {
    textarea.addEventListener('keydown', (e) => {
      if (e.key === 'Enter') {
        e.preventDefault();
        if (!e.shiftKey) {
          form.requestSubmit();
        }
      }
    });
  }

  form.addEventListener('submit', async (e) => {
    e.preventDefault();
    const url = form.action || window.location.href;
    const formData = new FormData(form);
    try {
      const res = await fetch(url, {
        method: 'POST',
        headers: {
          'X-CSRFToken': csrftoken,
          'X-Requested-With': 'XMLHttpRequest'
        },
        body: formData,
        credentials: 'same-origin'
      });
      if (!res.ok) return;
      const data = await res.json();
      form.reset();
      clearReplyPreview();

      const row = document.createElement('div');
      row.className = 'd-flex justify-content-end mb-2 message-row';
      row.innerHTML = `
        <div class="p-1 rounded message-bubble bg-dark text-white">
          <div>${data.content}</div>
        </div>
        <div class="message-actions ms-1">
          <button class="btn p-0 reply-btn">
            <i class="bi bi-reply"></i>
          </button>
          <button class="btn p-0 message-like" data-url="${data.like_url}">
            <svg aria-hidden="true" xmlns="http://www.w3.org/2000/svg" width="18" height="18" fill="none" viewBox="0 0 24 24">
              <path stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12.01 6.001C6.5 1 1 8 5.782 13.001L12.011 20l6.23-7C23 8 17.5 1 12.01 6.002Z" />
            </svg>
          </button>
        </div>
      `;
      const timestamp = document.createElement('div');
      timestamp.className = 'text-center text-muted small';
      timestamp.textContent = data.created_at;

      container.appendChild(row);
      container.appendChild(timestamp);
      scrollToBottom();

      const likeBtn = row.querySelector('.message-like');
      if (likeBtn) {
        likeBtn.addEventListener('click', async () => {
          const url = likeBtn.dataset.url;
          const countSpan = likeBtn.querySelector('.like-count');
          likeBtn.classList.toggle('liked');
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
              likeBtn.classList.toggle('liked');
              return;
            }
            if (res.ok) {
              const data = await res.json();
              likeBtn.classList.toggle('liked', data.liked);
              if (countSpan) countSpan.textContent = data.count;
            } else {
              likeBtn.classList.toggle('liked');
            }
          } catch (err) {
            console.error(err);
            likeBtn.classList.toggle('liked');
          }
        });
      }

      const replyBtn = row.querySelector('.reply-btn');
      if (replyBtn) attachReplyHandler(replyBtn);
    } catch (err) {
      console.error(err);
    }
  });
});
