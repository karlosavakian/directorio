// Simple emoji picker using EmojiButton library
// Requires EmojiButton via CDN

document.addEventListener('DOMContentLoaded', () => {
  const button = document.getElementById('emoji-button');
  const textarea = document.getElementById('id_content');
  if (!button || !textarea) return;

  const picker = new EmojiButton({ position: 'top-end' });
  picker.on('emoji', selection => {
    textarea.value += selection.emoji;
    textarea.focus();
  });

  button.addEventListener('click', () => picker.togglePicker(button));
});
