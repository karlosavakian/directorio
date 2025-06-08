document.addEventListener('DOMContentLoaded', function () {
    const form = document.getElementById('review-filter-form');
    if (!form) return;
    const sortDropdown = document.getElementById('sort-dropdown');
    const sortSelected = sortDropdown.querySelector('.selected-text');
    const sortMenu = document.getElementById('sort-menu');
    const sortInput = document.getElementById('sort-input');
    const reviewsContainer = document.getElementById('review-list');

    sortDropdown.querySelector('.selected').addEventListener('click', function (e) {
        e.stopPropagation();
        sortMenu.style.display = sortMenu.style.display === 'block' ? 'none' : 'block';
    });

    sortMenu.querySelectorAll('.dropdown-item').forEach(function (item) {
        item.addEventListener('click', function () {
            sortSelected.textContent = item.textContent;
            sortInput.value = item.dataset.value;
            sortMenu.style.display = 'none';
            const url = form.getAttribute('action');
            const params = new URLSearchParams(new FormData(form));
            fetch(url + '?' + params.toString(), {
                headers: {
                    'X-Requested-With': 'XMLHttpRequest'
                }
            })
                .then(res => res.text())
                .then(html => {
                    reviewsContainer.innerHTML = html;
                })
                .catch(err => console.error(err));
        });
    });

    document.addEventListener('click', function () {
        sortMenu.style.display = 'none';
    });
});
