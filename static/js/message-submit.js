document.addEventListener('DOMContentLoaded', () => {
  const form = document.getElementById('message-form');
  if (!form) return;

  const container = document.getElementById('message-container');
  const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]')?.value;
  const textarea = form.querySelector('textarea');
  const replyPreview = document.getElementById('reply-preview');
  const replyText = document.getElementById('reply-content');
  const replyClose = document.getElementById('reply-close');
  const replyInput = form.querySelector('[name="reply_to"]');

  const clearReplyPreview = () => {
    replyPreview?.classList.add('d-none');
    if (replyText) replyText.textContent = '';
    if (replyInput) replyInput.value = '';
  };
  replyClose?.addEventListener('click', () => {
    clearReplyPreview();
    textarea?.focus();
  });

  const attachReplyHandler = (btn) => {
    btn.addEventListener('click', () => {
      const row = btn.closest('.message-row');
      const contentElem = row?.querySelector('.message-content');
      let text = '';
      if (contentElem) {
        const span = contentElem.querySelector('span');
        text = span ? span.textContent.trim() : contentElem.textContent.trim();
      }
      const id = row?.dataset.id;
      if (text) {
        if (replyText) replyText.textContent = text;
        if (replyInput) replyInput.value = id || '';
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
        row.dataset.id = data.id;
        const quote = data.reply_to ? `<div class="bg-light p-1 rounded mb-1 text-dark">${data.reply_to}</div>` : '';
        const bubble = `
          <div class="p-1 rounded message-bubble col-md-5 text-wrap text-break bg-dark text-white">
            ${quote}
            <div class="message-content">${data.content}</div>
            <div class="text-end text-white small mt-1">${data.created_at}</div>
          </div>`;
        const actions = `
          <div class="message-actions ${data.sender_is_club ? 'me-1' : 'ms-1'}">
            <button class="btn p-0 reply-btn">
              <i class="bi bi-reply" style="transform:scaleX(-1);"></i>
            </button>
            <button class="btn p-0 message-like" data-url="${data.like_url}">
              <svg aria-hidden="true" xmlns="http://www.w3.org/2000/svg" width="18" height="18" fill="none" viewBox="0 0 24 24">
                <path stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12.01 6.001C6.5 1 1 8 5.782 13.001L12.011 20l6.23-7C23 8 17.5 1 12.01 6.002Z" />
              </svg>
            </button>
          </div>`;
        row.innerHTML = data.sender_is_club ? actions + bubble : bubble + actions;

      container.appendChild(row);
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
