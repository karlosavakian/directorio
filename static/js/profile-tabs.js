document.addEventListener('DOMContentLoaded', () => {
  const tabs = document.querySelectorAll('.profile-tab');
  const sections = document.querySelectorAll('.profile-section');
  const selects = document.querySelectorAll('.profile-tabs-select');
  const storageKey = 'activeTab:' + window.location.pathname;
  const baseTitle = document.title.split('|')[0].trim();

  function activate(tab) {
    tabs.forEach(t => t.classList.remove('active'));
    sections.forEach(s => s.classList.remove('active'));
    tab.classList.add('active');
    const target = tab.dataset.target;
    const sec = document.getElementById(target);
    if (sec) sec.classList.add('active');
    localStorage.setItem(storageKey, target);
    selects.forEach(s => (s.value = target));
    document.title = `${baseTitle} | ${tab.textContent.trim()}`;
  }

  tabs.forEach(t => {
    t.addEventListener('click', () => activate(t));
  });

  if (selects.length) {
    selects.forEach(sel => {
      sel.addEventListener('change', () => {
        const tab = document.querySelector(`.profile-tab[data-target="${sel.value}"]`);
        if (tab) activate(tab);
      });
    });
  }

  let target = localStorage.getItem(storageKey);
  let activeTab = tabs[0];
  if (target) {
    const stored = document.querySelector(`.profile-tab[data-target="${target}"]`);
    if (stored) activeTab = stored;
  } else {
    activeTab = document.querySelector('.profile-tab.active') || tabs[0];
  }
  if (activeTab) activate(activeTab);
});
