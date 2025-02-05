document.querySelectorAll('.toggle-details').forEach(button => {
    button.addEventListener('click', () => {
        const details = button.nextElementSibling;
        details.classList.toggle('hidden');
        details.classList.toggle('visible');

        button.textContent = details.classList.contains('visible') ? 'Nascondi dettagli' : 'Mostra dettagli';
    });
});

// FUNZIONE DELLA PROF PER CREARE UN'ISTANZA DI PRODOTTO
function Prodotto(nome, prezzo, categoria) {
    this.nome = nome;
    this.prezzo = prezzo;
    this.categoria = categoria;

// MOSTRA DETTAGLI PRODOTTO
    this.mostraDettagli = function() {
        return `Prodotto: ${this.nome}, Prezzo: €${this.prezzo.toFixed(2)}, Categoria: ${this.categoria}`;
    };
}

// COSTRUTTORE CARRELLO
function Carrello() {
    this.prodotti = [];
    this.totale = 0;

    // AGGIUNGI OGGETTO AL CARRELLO
    this.aggiungiProdotto = function(prodotto) {
        this.prodotti.push(prodotto);
        this.totale += prodotto.prezzo;
    };

    // MOSTRA TOTALE CARRELLO
    this.mostraTotale = function() {
        return `€${this.totale.toFixed(2)}`;
    };
}

// CREAZIONE NUOVO CARRELLO
var carrello = new Carrello();

// AGGIUNGI PRODOTTO E MOSTRA DETTAGLI
function aggiungiProdottoAlCarrello() {

    // RECUPERO VALORI DAL FORM
    var nomeProdotto = document.getElementById("nomeProdotto").value;
    var prezzoProdotto = parseFloat(document.getElementById("prezzoProdotto").value);
    var categoriaProdotto = document.getElementById("categoriaProdotto").value;

    // CREAZIONE ISTANZA DI PRODOTTO
    var nuovoProdotto = new Prodotto(nomeProdotto, prezzoProdotto, categoriaProdotto);

    // AGGIUNTA AL CARRELLO
    carrello.aggiungiProdotto(nuovoProdotto);

    // MOSTRA I DETTAGLI
    document.getElementById("dettagliProdotto").textContent = nuovoProdotto.mostraDettagli();

    // MOSTRA IL TOTALE
    document.getElementById("totaleCarrello").textContent = carrello.mostraTotale();

    console.log(nuovoProdotto);
    console.log(carrello);
}