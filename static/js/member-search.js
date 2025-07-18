document.addEventListener('DOMContentLoaded', () => {
  const form = document.getElementById('member-search-form');
  const input = document.getElementById('member-search-input');
  const searchBtn = form.querySelector('.search-icon');
  const closeBtn = form.querySelector('.close-icon');
  if (!form || !input || !searchBtn || !closeBtn) return;

  if (input.value) {
    form.classList.add('open');
  }

  const openSearch = () => {
    form.classList.add('open');
    input.focus();
  };

  const closeSearch = () => {
    form.classList.remove('open');
    input.value = '';
    filter();
  };

  searchBtn.addEventListener('click', (e) => {
    if (!form.classList.contains('open')) {
      e.preventDefault();
      openSearch();
    }
  });

  closeBtn.addEventListener('click', closeSearch);

  input.addEventListener('blur', () => {
    if (!input.value) {
      form.classList.remove('open');
    }
  });
  const rows = Array.from(document.querySelectorAll('#tab-members tbody tr'));
  const emptyRow = document.querySelector('#tab-members tbody .no-members-row');

  const filter = () => {
    const query = input.value.toLowerCase().trim();
    let shown = 0;
    rows.forEach(row => {
      if (row.classList.contains('no-members-row')) return;
      const text = row.innerText.toLowerCase();
      if (!query || text.includes(query)) {
        row.style.display = '';
        shown++;
      } else {
        row.style.display = 'none';
      }
    });
    if (emptyRow) {
      emptyRow.style.display = shown ? 'none' : '';
    }
  };

  input.addEventListener('input', filter);
});
