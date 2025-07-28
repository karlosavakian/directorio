document.addEventListener("DOMContentLoaded", function () {
    const forms = document.querySelectorAll("#main-search-form");
    const stopWords = ["a", "de", "la", "el", "en", "y"];

    forms.forEach(form => {
        const input = form.querySelector("#search-input");
        if (!input) return;

        form.addEventListener("submit", function (e) {
            const text = input.value.trim().toLowerCase();
            const isValid = text.length >= 3 && !stopWords.includes(text);

            if (!isValid) {
                e.preventDefault();
                form.classList.add("form-error");
                setTimeout(() => {
                    form.classList.remove("form-error");
                }, 600);
            }
        });
    });
});
