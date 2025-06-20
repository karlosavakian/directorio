document.addEventListener('DOMContentLoaded', () => {
  const tabs = document.querySelectorAll('#clubTabs button[data-bs-toggle="tab"]');
  if (!tabs.length) return;

  const storageKey = 'clubActiveTab:' + window.location.pathname;

  tabs.forEach(tab => {
    tab.addEventListener('shown.bs.tab', e => {
      localStorage.setItem(storageKey, e.target.getAttribute('data-bs-target'));
    });
  });

  const active = localStorage.getItem(storageKey);
  if (active) {
    const stored = document.querySelector(`#clubTabs button[data-bs-target="${active}"]`);
    if (stored) {
      const bootstrapTab = new bootstrap.Tab(stored);
      bootstrapTab.show();
    }
  }
});
