document.addEventListener("DOMContentLoaded", function () {
    const form = document.getElementById("main-search-form");
    const input = document.getElementById("search-input");

    const stopWords = ["a", "de", "la", "el", "en", "y"];

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
