  document.addEventListener("DOMContentLoaded", function () {
            document.querySelectorAll(".star-rating").forEach(function (ratingDiv) {
                const field = ratingDiv.dataset.field;
                const input = document.getElementById("input-" + field);
                const score = parseInt(ratingDiv.dataset.score) || 0;
        
                for (let i = 1; i <= 5; i++) {
                    const star = document.createElement("span");
                    star.classList.add("star");
                    star.innerHTML = "&#9733;"; // Unicode black star
                    star.dataset.value = i;
                    star.style.cursor = "pointer";
                    star.style.fontSize = "24px";
                    star.style.color = i <= score ? "#000" : "#ccc";
        
                    star.addEventListener("click", function () {
                        input.value = i;
                        const stars = ratingDiv.querySelectorAll(".star");
                        stars.forEach((s, idx) => {
                            s.style.color = idx < i ? "#000" : "#ccc";
                        });
                    });
        
                    ratingDiv.appendChild(star);
                }
            });
        });

        
        