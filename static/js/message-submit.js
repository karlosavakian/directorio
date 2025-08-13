document.addEventListener('DOMContentLoaded', () => {
  const form = document.getElementById('message-form');
  const thread = document.getElementById('message-thread');

  const scrollToBottom = () => {
    if (thread) {
      thread.scrollTop = thread.scrollHeight;
    }
  };

  if (form && thread) {
    const textarea = form.querySelector('textarea[data-autosize]');
    if (textarea && typeof autosize === 'function') {
      autosize(textarea);
    }
    scrollToBottom();

    form.addEventListener('submit', async (e) => {
      e.preventDefault();
      const content = textarea.value.trim();
      if (!content) return;

      const url = form.action || window.location.href;
      const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]')?.value;
      const formData = new FormData();
      formData.append('content', content);

      try {
        await fetch(url, {
          method: 'POST',
          headers: {
            'X-CSRFToken': csrftoken,
            'X-Requested-With': 'XMLHttpRequest'
          },
          body: formData
        });

        const wrapper = document.createElement('div');
        wrapper.className = 'd-flex justify-content-end mb-2 message-row';
        wrapper.innerHTML = `
          <div class="p-1 rounded message-bubble bg-dark text-white">
            <div>${content}</div>
          </div>
        `;
        thread.appendChild(wrapper);
        const timestamp = document.createElement('div');
        timestamp.className = 'text-center text-muted small';
        timestamp.textContent = 'justo ahora';
        thread.appendChild(timestamp);

        form.reset();
        if (typeof autosize !== 'undefined') {
          autosize.update(textarea);
        }
        scrollToBottom();
      } catch (err) {
        console.error(err);
      }
    });
  } else {
    scrollToBottom();
  }
});
