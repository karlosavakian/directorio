
  const sortDropdown = document.getElementById("sort-dropdown");
  const sortSelected = sortDropdown.querySelector(".selected-text");
  const sortMenu = document.getElementById("sort-menu");
  const sortInput = document.getElementById("sort-input");

  sortDropdown.querySelector(".selected").addEventListener("click", (e) => {
    e.stopPropagation();
    sortMenu.style.display = sortMenu.style.display === "block" ? "none" : "block";
  });

  sortMenu.querySelectorAll(".dropdown-item").forEach(item => {
    item.addEventListener("click", () => {
      sortSelected.textContent = item.textContent;
      sortInput.value = item.dataset.value;
      sortMenu.style.display = "none";
      sortDropdown.closest("form").submit();
    });
  });

  document.addEventListener("click", () => {
    sortMenu.style.display = "none";
  }); 


  