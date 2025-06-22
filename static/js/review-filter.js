document.addEventListener('DOMContentLoaded', function () {
    const form = document.getElementById('review-filter-form');
    if (!form) return;
    const sortDropdown = document.getElementById('sort-dropdown');
    const sortSelected = sortDropdown.querySelector('.selected-text');
    const sortMenu = document.getElementById('sort-menu');
    const sortInput = document.getElementById('sort-input');
    const pageInput = document.getElementById('page-input');
    const reviewsContainer = document.getElementById('review-list');

    function fetchReviews(page) {
        if (page) pageInput.value = page;
        const url = form.getAttribute('action');
        const params = new URLSearchParams(new FormData(form));
        fetch(url + '?' + params.toString(), {
            headers: {
                'X-Requested-With': 'XMLHttpRequest'
            }
        })
            .then(res => res.text())
            .then(html => {
                reviewsContainer.classList.remove('show');
                reviewsContainer.innerHTML = html;
                requestAnimationFrame(() => reviewsContainer.classList.add('show'));
            })
            .catch(err => console.error(err));
    }

    sortDropdown.querySelector('.selected').addEventListener('click', function (e) {
        e.stopPropagation();
        sortMenu.style.display = sortMenu.style.display === 'block' ? 'none' : 'block';
    });

    sortMenu.querySelectorAll('.dropdown-item').forEach(function (item) {
        item.addEventListener('click', function () {
            sortSelected.textContent = item.textContent;
            sortInput.value = item.dataset.value;
            pageInput.value = 1;
            sortMenu.style.display = 'none';
            fetchReviews();
        });
    });

    document.addEventListener('click', function () {
        sortMenu.style.display = 'none';
    });

    reviewsContainer.addEventListener('click', function (e) {
        const link = e.target.closest('.page-link');
        if (link) {
            e.preventDefault();
            fetchReviews(link.dataset.page);
        }
    });
});
