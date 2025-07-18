document.addEventListener('DOMContentLoaded', () => {
  const input = document.querySelector('#member-search-form input[name="q"]');
  const wrapper = document.querySelector('.member-search-wrapper');
  const toggleBtn = document.getElementById('member-search-toggle');
  if (!input || !wrapper || !toggleBtn) return;

  toggleBtn.addEventListener('click', () => {
    wrapper.classList.toggle('show');
    if (wrapper.classList.contains('show')) {
      input.focus();
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

  const clearBtn = document.querySelector('#member-search-form .clear-btn');
  if (clearBtn) {
    clearBtn.addEventListener('click', () => {
      input.value = '';
      filter();
    });
  }
});
