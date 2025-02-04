document.querySelectorAll('.toggle-details').forEach(button => {
    button.addEventListener('click', () => {
        const details = button.nextElementSibling;
        details.classList.toggle('hidden');
        details.classList.toggle('visible');

        button.textContent = details.classList.contains('visible') ? 'Nascondi dettagli' : 'Mostra dettagli';
    });
});