document.addEventListener('DOMContentLoaded', () => {
  const tabs = document.querySelectorAll('.profile-tab[data-target]');
  const sections = document.querySelectorAll('.profile-section');
  if (!tabs.length) return;
  const storageKey = 'activeTab:' + window.location.pathname;

  function activate(tab) {
    const target = tab.dataset.target;
    if (!target) return;

    tabs.forEach(t => t.classList.remove('active'));
    sections.forEach(s => s.classList.remove('active'));
    tab.classList.add('active');
    const sec = document.getElementById(target);
    if (sec) sec.classList.add('active');
    localStorage.setItem(storageKey, target);
  }

  tabs.forEach(t => {
    t.addEventListener('click', () => activate(t));
  });

  let target = localStorage.getItem(storageKey);
  let activeTab = null;
  if (target) {
    const stored = document.querySelector(`.profile-tab[data-target="${target}"]`);
    if (stored) activeTab = stored;
  }
  if (!activeTab) {
    activeTab = document.querySelector('.profile-tab.active[data-target]') || tabs[0];
  }
  if (activeTab) activate(activeTab);
});
