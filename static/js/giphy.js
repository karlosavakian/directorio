(document => {
  const btn = document.getElementById('giphyBtn');
  const modalEl = document.getElementById('giphyModal');
  if (!btn || !modalEl) return;
  const modal = new bootstrap.Modal(modalEl);
  const form = modalEl.querySelector('form');
  const results = modalEl.querySelector('.giphy-results');
  const input = modalEl.querySelector('input[name="q"]');
  const textarea = document.getElementById('id_contenido');

  async function loadGifs(query = '') {
    try {
      const endpoint = query
        ? `https://api.giphy.com/v1/gifs/search?api_key=dc6zaTOxFJmzC&limit=24&q=${encodeURIComponent(query)}`
        : `https://api.giphy.com/v1/gifs/trending?api_key=dc6zaTOxFJmzC&limit=24`;
      const res = await fetch(endpoint);
      const data = await res.json();
      results.innerHTML = data.data
        .map(g => `<img src="${g.images.fixed_height.url}" data-url="${g.images.original.url}" class="giphy-gif img-fluid" style="cursor:pointer;width:100px;">`)
        .join('');
    } catch (err) {
      console.error(err);
    }
  }

  btn.addEventListener('click', () => {
    loadGifs();
    modal.show();
  });

  form.addEventListener('submit', e => {
    e.preventDefault();
    loadGifs(input.value);
  });

  results.addEventListener('click', e => {
    if (e.target.classList.contains('giphy-gif')) {
      const url = e.target.dataset.url;
      if (textarea) textarea.value += ` <img src="${url}">`;
      modal.hide();
    }
  });
})(document);
