document.addEventListener('DOMContentLoaded', () => {
  const form = document.getElementById('message-form');
  if (!form) return;

  const container = document.getElementById('message-container');
  const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]')?.value;
  const textarea = form.querySelector('textarea');
  const replyPreview = document.getElementById('reply-preview');
  const replyText = document.getElementById('reply-content');
  const replyUsername = document.getElementById('reply-username');
  const replyClose = document.getElementById('reply-close');
  const replyInput = form.querySelector('[name="reply_to"]');

  const clearReplyPreview = () => {
    replyPreview?.classList.add('d-none');
    if (replyText) replyText.textContent = '';
    if (replyUsername) replyUsername.textContent = '';
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
      const sender = row?.dataset.sender || '';
      if (text) {
        if (replyText) replyText.textContent = text;
        if (replyUsername) replyUsername.textContent = sender;
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
        row.dataset.sender = data.sender;
        const quote = data.reply_to ? `<div class="message-reply rounded text-white mb-2"><div class="fw-medium small">${data.reply_to.sender}</div><span class="small test-white fw-light fst-italic">${data.reply_to.content}</span></div>` : '';

const bubble = `
  <div class="rounded message-bubble text-wrap text-break bg-dark text-white">
    ${quote}
    <div class="message-content d-flex justify-content-between align-items-center">
      <span>${data.content}</span>
      <span style="font-size:10px;" class="small text-nowrap ms-2 mt-auto align-self-end text-light">${data.created_at}</span>
    </div>
  </div>`;
const actions = `
  <div class="message-actions me-1">
    <button class="btn p-0 reply-btn">
      <svg class="w-6 h-6" aria-hidden="true" xmlns="http://www.w3.org/2000/svg" width="18" height="18" fill="none" viewBox="0 0 24 24" style="transform:scaleX(-1);">
        <path stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M14.5 8.046H11V6.119c0-.921-.9-1.446-1.524-.894l-5.108 4.49a1.2 1.2 0 0 0 0 1.739l5.108 4.49c.624.556 1.524.027 1.524-.893v-1.928h2a3.023 3.023 0 0 1 3 3.046V19a5.593 5.593 0 0 0-1.5-10.954Z"/>
      </svg>
    </button>
    <button class="btn p-0 message-like" data-url="${data.like_url}">
      <svg aria-hidden="true" xmlns="http://www.w3.org/2000/svg" width="18" height="18" fill="none" viewBox="0 0 24 24">
        <path stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12.01 6.001C6.51 1 1 8 5.782 13.001L12.011 20l6.23-7C23 8 17.5 1 12.01 6.002Z" />
      </svg>
    </button>
  </div>`;
row.innerHTML = actions + bubble;

      container.appendChild(row);
      scrollToBottom();

      const likeBtn = row.querySelector('.message-like');
      if (likeBtn && window.attachMessageLike) {
        window.attachMessageLike(likeBtn);
      }

      const replyBtn = row.querySelector('.reply-btn');
      if (replyBtn) attachReplyHandler(replyBtn);
    } catch (err) {
      console.error(err);
    }
  });
});
