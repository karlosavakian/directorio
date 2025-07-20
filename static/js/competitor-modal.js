document.addEventListener('DOMContentLoaded', () => {
  const addEl = document.getElementById('addCompetitorModal');
  const addModal = addEl ? new bootstrap.Modal(addEl) : null;
  const btn = document.querySelector('.add-competitor-btn');
  if (btn) {
    btn.addEventListener('click', () => {
      const slug = btn.dataset.clubSlug;
      fetch(`/clubs/${slug}/competidor/nuevo/`, {
        headers: { 'X-Requested-With': 'XMLHttpRequest' }
      })
        .then(res => res.text())
        .then(html => {
          if (addEl) {
            addEl.querySelector('.modal-body').innerHTML = html;
            if (window.initAvatarDropzones) {
              window.initAvatarDropzones(addEl);
            }
            if (window.initSelectLabels) {
              window.initSelectLabels(addEl);
            }
            if (window.initAgeCategory) {
              window.initAgeCategory(addEl);
            }
            const membersDataEl = addEl.querySelector('#competitor-members');
            let members = [];
            if (membersDataEl) {
              try {
                members = JSON.parse(membersDataEl.textContent);
              } catch (e) {}
            }
            const searchForm = addEl.querySelector('#competitor-member-search-form');
            const searchInput = addEl.querySelector('#competitor-member-search');
            const resultsEl = addEl.querySelector('#competitor-member-results');
            const searchBtn = searchForm ? searchForm.querySelector('.search-icon') : null;
            const closeBtn = searchForm ? searchForm.querySelector('.close-icon') : null;
            function renderResults(query) {
              if (!resultsEl) return;
              resultsEl.innerHTML = '';
              if (!query) return;
              const q = query.toLowerCase();
              members.filter(m => (`${m.nombre} ${m.apellidos}`.toLowerCase().includes(q))).slice(0,5).forEach(m => {
                const li = document.createElement('li');
                li.className = 'list-group-item list-group-item-action';
                li.textContent = `${m.nombre} ${m.apellidos}`;
                li.addEventListener('click', () => {
                  const nameField = addEl.querySelector(`input[name='nombre']`);
                  const lastField = addEl.querySelector(`input[name='apellidos']`);
                  if (nameField) nameField.value = m.nombre || '';
                  if (lastField) lastField.value = m.apellidos || '';
                  const sexoField = addEl.querySelector(`select[name='sexo']`);
                  if (sexoField) sexoField.value = m.sexo || '';
                  const pesoField = addEl.querySelector(`input[name='peso_kg']`);
                  if (pesoField) pesoField.value = m.peso || '';
                  const alturaField = addEl.querySelector(`input[name='altura_cm']`);
                  if (alturaField) alturaField.value = m.altura || '';
                  resultsEl.innerHTML = '';
                  searchInput.value = '';
                });
                resultsEl.appendChild(li);
              });
            }
            if (searchInput) {
              searchInput.addEventListener('input', () => {
                renderResults(searchInput.value);
              });
              searchInput.addEventListener('blur', () => {
                if (!searchInput.value && searchForm) searchForm.classList.remove('open');
              });
            }
            if (searchBtn) {
              searchBtn.addEventListener('click', e => {
                if (searchForm && !searchForm.classList.contains('open')) {
                  e.preventDefault();
                  searchForm.classList.add('open');
                  searchInput && searchInput.focus();
                }
              });
            }
            if (closeBtn) {
              closeBtn.addEventListener('click', () => {
                if (resultsEl) resultsEl.innerHTML = '';
                if (searchInput) searchInput.value = '';
                if (searchForm) searchForm.classList.remove('open');
              });
            }
            const form = addEl.querySelector('form');
            form.addEventListener('submit', e => {
              e.preventDefault();
              const fd = new FormData(form);
              fetch(form.action, {
                method: 'POST',
                headers: { 'X-Requested-With': 'XMLHttpRequest' },
                body: fd
              }).then(() => window.location.reload());
            });
            addModal.show();
          }
        });
    });
  }
});
