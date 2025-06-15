document.addEventListener('DOMContentLoaded', () => {
  const tabs = document.querySelectorAll('.profile-tab');
  const sections = document.querySelectorAll('.profile-section');

  function activate(tab) {
    tabs.forEach(t => t.classList.remove('active'));
    sections.forEach(s => s.classList.remove('active'));
    tab.classList.add('active');
    const target = tab.dataset.target;
    const sec = document.getElementById(target);
    if (sec) sec.classList.add('active');
  }

  tabs.forEach(t => {
    t.addEventListener('click', () => activate(t));
  });

  const activeTab = document.querySelector('.profile-tab.active') || tabs[0];
  if (activeTab) activate(activeTab);
});
