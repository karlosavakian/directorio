document.addEventListener('DOMContentLoaded', () => {
  const planCards = document.querySelectorAll('.plan-card');
  planCards.forEach(card => {
    const input = card.querySelector('input');
    if (input.checked) {
      card.classList.add('active');
    }
    card.addEventListener('click', () => {
      input.checked = true;
      planCards.forEach(c => c.classList.toggle('active', c === card));
    });
  });
});
