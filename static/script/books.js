// ADD BOOK //
document.getElementById("addBookForm").addEventListener("submit", addBook);

async function addBook(event){
    event.preventDefault() //Preventing page refreshing

    let Title = document.getElementById("addTitle").value
    let Author = document.getElementById("addAuthor").value
    let Genre = document.getElementById("addGenre").value
    let Height = document.getElementById("addHeight").value
    let Publisher = document.getElementById("addPublisher").value

    let response = await fetch("api/books", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({Title, Author, Genre, Height, Publisher})
    })

    let result = await response.json()
    if(response.ok) {
        alert("Book successfully added")
    }
    else {
        alert(`Error: ${result.error}`)
    }
}

// SEARCH BOOK //

document.getElementById("searchBookForm").addEventListener("submit", searchBook);

async function searchBook(event) {
    event.preventDefault();

    let title = document.getElementById("searchTitle").value.trim();
    let author = document.getElementById("searchAuthor").value.trim();

    if (!title && !author) {
        alert("Inserisci almeno il titolo o l'autore per effettuare la ricerca.");
        return;
    }

    try {
        let response = await fetch(`/api/books/search?title=${encodeURIComponent(title)}&author=${encodeURIComponent(author)}`);
        let result = await response.json();

        if (response.ok) {
            displayBooks(result.books); // Funzione per mostrare i risultati
        } else {
            alert(`Errore: ${result.error}`);
        }
    } catch (error) {
        console.error("Errore nella richiesta:", error);
    }
}

function displayBooks(books) {
    const table = document.getElementById("resultsTable");
    table.innerHTML = ""; // Pulisce la tabella prima di mostrare i nuovi risultati

    if (books.length === 0) {
        table.innerHTML = "<tr><td colspan='5'>Nessun libro trovato.</td></tr>";
        return;
    }

    table.innerHTML = `
        <tr>
            <th>Titolo</th>
            <th>Autore</th>
            <th>Genere</th>
            <th>Pagine</th>
            <th>Casa Editrice</th>
        </tr>
    `;

    books.forEach(book => {
        let row = `
            <tr>
                <td>${book.Title}</td>
                <td>${book.Author}</td>
                <td>${book.Genre}</td>
                <td>${book.Height}</td>
                <td>${book.Publisher}</td>
            </tr>
        `;
        table.innerHTML += row;
    });
}

// REMOVE BOOK //

document.getElementById("removeBookForm").addEventListener("submit", removeBook);

async function removeBook(event) {
    event.preventDefault();

    let Title = document.getElementById("removeTitle").value;
    let Author = document.getElementById("removeAuthor").value;
    let Genre = document.getElementById("removeGenre").value;
    let Height = document.getElementById("removeHeight").value;
    let Publisher = document.getElementById("removePublisher").value;

    let response = await fetch("/api/books", {
        method: "DELETE",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({Title, Author, Genre, Height, Publisher})
    });

    let result = await response.json();
    if (response.ok) {
        alert("Book successfully removed");
    } else {
        alert(`Error: ${result.error}`);
    }
}