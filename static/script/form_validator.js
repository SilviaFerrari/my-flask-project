document.getElementById("js_check_form").addEventListener("submit", checkForm);

async function checkForm(event){

    let name = document.getElementById("js_username").value
    let password = document.getElementById("js_password").value
    let email = document.getElementById("js_email").value

    let errors = [];

    // Verifica se tutti i campi sono compilati
    if (!name || !password || !email) {
        errors.push('Tutti i campi devono essere compilati.');
    }

    // Verifica nome (solo caratteri alfabetici)
    if (!/^[A-Za-z\s]+$/.test(name)) {
        errors.push('Il nome deve contenere solo lettere.');
    }

    // Verifica password (minimo 8 caratteri, una lettera maiuscola, una minuscola, un numero)
    if (!/^(?=.*[a-z])(?=.*[A-Z])(?=.*\d).{8,}$/.test(password)) {
        errors.push('La password deve contenere almeno 8 caratteri, una lettera maiuscola, una minuscola e un numero.');
    }

    // Verifica email
    if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email)) {
        errors.push('Inserisci un\'email valida.');
    }

    if (errors.length > 0) {
        event.preventDefault(); // Blocca l'invio del form
        alert(errors.join('\n'));
    }
}