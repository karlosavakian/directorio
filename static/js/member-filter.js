document.addEventListener('DOMContentLoaded', () => {
  // Previously the form submitted automatically on input change.
  // Se deshabilita el auto envío para que el filtrado solo ocurra
  // al presionar el botón correspondiente.
  const form = document.getElementById('member-filter-form');
  if (!form) return;
  // No listeners: el usuario debe pulsar "Filtrar".
});
