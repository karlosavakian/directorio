document.addEventListener('DOMContentLoaded', () => {
    document.querySelectorAll('.star-rating').forEach(container => {
        const name = container.dataset.field || container.dataset.name;
        if (!name) return;

        const id = 'input-' + name;
        let input = container.querySelector('input[name="' + name + '"]') ||
                    document.getElementById(id);

        if (!input) {
            input = document.createElement('input');
            input.type = 'hidden';
            input.name = name;
            input.id = id;
            container.appendChild(input);
        }

        let rating = parseInt(container.dataset.score || input.value || 0);
        if (isNaN(rating)) rating = 0;
        input.value = rating;

        const starPath =
            'M12 17.27L18.18 21l-1.64-7.03L22 9.24l-7.19-.61L12 2 9.19 8.63 2 9.24l5.46 4.73L5.82 21z';
        const stars = [];

        for (let i = 1; i <= 5; i++) {
            const svg = document.createElementNS('http://www.w3.org/2000/svg', 'svg');
            svg.setAttribute('width', '24');
            svg.setAttribute('height', '24');
            svg.setAttribute('viewBox', '0 0 24 24');
            svg.classList.add('star');
            svg.dataset.value = i;
            svg.setAttribute('tabindex', '0');

            const path = document.createElementNS('http://www.w3.org/2000/svg', 'path');
            path.setAttribute('d', starPath);
            svg.appendChild(path);

            svg.addEventListener('mouseenter', () => draw(i));
            svg.addEventListener('focus', () => draw(i));
            svg.addEventListener('mouseleave', () => draw(rating));
            svg.addEventListener('click', () => set(i));
            svg.addEventListener('keydown', e => {
                if (e.key === 'ArrowLeft') {
                    set(Math.max(1, rating - 1));
                    stars[rating - 1].focus();
                } else if (e.key === 'ArrowRight') {
                    set(Math.min(5, rating + 1));
                    stars[rating - 1].focus();
                } else if (e.key === ' ' || e.key === 'Enter') {
                    set(i);
                }
            });

            container.appendChild(svg);
            stars.push(svg);
        }

        draw(rating);

        function draw(val) {
            stars.forEach((star, idx) => {
                star.classList.toggle('active', idx < val);
            });
        }

        function set(val) {
            rating = val;
            input.value = val;
            draw(val);
        }
    });
});