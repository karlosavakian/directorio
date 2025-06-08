
 document.addEventListener('DOMContentLoaded', function () {
    const stars = document.querySelectorAll('.star-rating');
    stars.forEach(container => {
        const inputName = container.dataset.name;
        for (let i = 1; i <= 5; i++) {
            const svg = document.createElementNS("http://www.w3.org/2000/svg", "svg");
            svg.setAttribute("width", "24");
            svg.setAttribute("height", "24");
            svg.setAttribute("viewBox", "0 0 24 24");
            svg.setAttribute("fill", "#e0e0e0");
            svg.setAttribute("stroke", "#888");
            svg.classList.add("star");
            svg.dataset.value = i;

            svg.innerHTML = `<path d="M12 17.27L18.18 21l-1.64-7.03L22 9.24l-7.19-.61L12 2 9.19 8.63 2 9.24l5.46 4.73L5.82 21z"/>`;

            svg.addEventListener("click", () => {
                container.querySelectorAll("svg").forEach(s => s.classList.remove("active"));
                for (let j = 1; j <= i; j++) {
                    container.querySelector(`svg[data-value="${j}"]`).classList.add("active");
                }
                const old = container.querySelector("input[type=hidden]");
                if (old) old.remove();
                const input = document.createElement("input");
                input.type = "hidden";
                input.name = inputName;
                input.value = i;
                container.appendChild(input);
            });

            container.appendChild(svg);
        }
    });
});