
document.addEventListener('DOMContentLoaded', function () {
    const starsGroups = document.querySelectorAll('.star-rating');
    starsGroups.forEach(container => {
        const inputName = container.dataset.name;
        let selected = 0;
        const stars = [];
        for (let i = 1; i <= 5; i++) {
            const svg = document.createElementNS('http://www.w3.org/2000/svg', 'svg');
            svg.setAttribute('width', '24');
            svg.setAttribute('height', '24');
            svg.setAttribute('viewBox', '0 0 24 24');
            svg.setAttribute('fill', '#e0e0e0');
            svg.setAttribute('stroke', '#888');
            svg.classList.add('star');
            svg.dataset.value = i;
            svg.innerHTML = '<path d="M12 17.27L18.18 21l-1.64-7.03L22 9.24l-7.19-.61L12 2 9.19 8.63 2 9.24l5.46 4.73L5.82 21z"/>';

            svg.addEventListener('mouseenter', () => highlight(i));
            svg.addEventListener('click', () => {
                selected = i;
                updateInput(i);
            });
            stars.push(svg);
            container.appendChild(svg);
        }

        container.addEventListener('mouseleave', () => highlight(selected));

        function highlight(val) {
            stars.forEach((s, idx) => {
                if (idx < val) {
                    s.classList.add('active');
                } else {
                    s.classList.remove('active');
                }
            });
        }

        function updateInput(val) {
            let input = container.querySelector('input[name="' + inputName + '"]');
            if (!input) {
                input = document.createElement('input');
                input.type = 'hidden';
                input.name = inputName;
                container.appendChild(input);
            }
            input.value = val;
        }
    });
});