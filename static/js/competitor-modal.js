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
            const membersDataEl = addEl.querySelector('#competitor-members');
            let members = [];
            if (membersDataEl) {
              try {
                members = JSON.parse(membersDataEl.textContent);
              } catch (e) {}
            }
            const searchInput = addEl.querySelector('#competitor-member-search');
            const resultsEl = addEl.querySelector('#competitor-member-results');
            const closeBtn = addEl.querySelector('#competitor-member-search-form .close-icon');
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
                  if (nameField) nameField.value = `${m.nombre} ${m.apellidos}`;
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
            }
            if (closeBtn) {
              closeBtn.addEventListener('click', () => {
                if (resultsEl) resultsEl.innerHTML = '';
                if (searchInput) searchInput.value = '';
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
