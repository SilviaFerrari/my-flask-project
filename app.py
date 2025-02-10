# se clicchiamo sul sito dei link, vediamo su terminale le GET
# e le rischieste con i rispettivi codici

from flask import Flask, render_template, request, jsonify, send_from_directory
import csv
import os.path

#
# FUNZIONE PER CARICARE DA CSV
#

def load_csv_data(file_path):
    csv_data = []
    csv_path = os.path.join(os.path.dirname(__file__), file_path)
    try:
        with open(csv_path, mode='r', encoding='utf-8') as csv_file:
            csv_reader = csv.DictReader(csv_file)
            for row in csv_reader:
                csv_data.append(row)
            return csv_data
    except FileNotFoundError:
        print(f"File non trovato: {csv_path}")
        return []
    except Exception as e:
        print(f"Errore imprevisto durante la lettura di {csv_path}: {e}")
        return []

#
# ROUTE DELLE PAGINE HTML
#
app = Flask(__name__)
@app.route('/') #home page
def index():
    return render_template('index.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')

@app.route('/react') #home page
def react():
    return send_from_directory("static", "react_index.html")

@app.route('/team')
def team():
    team_members = load_csv_data('data/team.csv')
    products_data = load_csv_data('data/products.csv')
    return render_template('team.html', products_data=products_data, team_members=team_members)

@app.route('/about') # contains also the books list
def about():
    books_data = load_csv_data('data/books.csv')
    return render_template('about.html', books_data=books_data)

@app.route('/events')
def events():
    events_data = load_csv_data('data/events.csv')
    return render_template('events.html', events_data=events_data)

@app.route('/events/<event_code>', methods=['GET'])
def details(event_code):
    events_data = load_csv_data('data/events.csv')
    event = next((e for e in events_data if e['code'] == event_code), None)
    if event:
        return render_template('details.html', event=event)
    return "Evento non trovato", 404

#
# FUNZIONALITA' API
#

@app.route('/api/events', methods=['GET'])
def get_events():
    events_data = load_csv_data('data/events.csv')
    return jsonify(events_data)

@app.route('/api/event/<event_code>', methods=['GET'])
def get_event(event_code):
    events_data = load_csv_data('data/events.csv')
    event = next((e for e in events_data if e['code'] == event_code), None)
    if event:
        return jsonify(event)
    return jsonify({'error': 'Evento non trovato'}), 404


# Funzione per prenotare un posto
@app.route('/api/booking/<event_code>', methods=['POST'])
def book_event(event_code):
    events_data = load_csv_data('data/events.csv')
    for event in events_data:
        if event['code'] == event_code:
            available_places = int(event['available_places'])
            if available_places > 0:
                event['available_places'] = available_places - 1
                write_events(events_data)
                return jsonify({'success': True, 'message': 'Posto prenotato con successo!'})
            return jsonify({'success': False, 'message': 'Posti esauriti!'}), 400
    return jsonify({'success': False, 'message': 'Evento non trovato!'}), 404

# Funzione per scrivere nel file CSV
def write_events(events_data):
    csv_path = os.path.join(os.path.dirname(__file__), 'data/events.csv')
    with open(csv_path, mode='w', newline='', encoding='utf-8') as csv_file:
        fieldnames = ['code', 'name', 'sport', 'date', 'place', 'available_places']
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(events_data)


# LIBRI #

@app.route('/api/books', methods=['GET'])
def api_books():
    books_data = load_csv_data('data/books.csv')
    return jsonify(books_data)

# API PER CERCARE UN LIBRO PER AUTORE O TITOLO
# GET ci restituisce una risorsa così com'è
@app.route('/api/books/search', methods=['GET'])
def search_books():
    try:
        title_query = request.args.get('title', '').strip().lower()
        author_query = request.args.get('author', '').strip().lower()

        # Carica i dati dal CSV
        books = load_csv_data('data/books.csv')

        # Filtra i libri in base al titolo o all'autore
        filtered_books = [
            book for book in books
            if (title_query == book["Title"].strip().lower() if title_query else True) and
               (author_query == book["Author"].strip().lower() if author_query else True)

            # guarda se title_query è contenuto nel titolo e non se sono uguali
            #if (title_query in book["Title"].strip().lower() if title_query else True) and
            #   (author_query in book["Author"].strip().lower() if author_query else True)
        ]

        return jsonify({"books": filtered_books}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500


# API PER AGGIUNGERE UN LIBRO CON COTROLLO DEI DOPPIONI
# POST va a modificare una risorsa
@app.route('/api/books', methods=['POST'])
def add_book_api():
    try:
        add_book = request.get_json()                  # Get data from the request
        books_data = load_csv_data('data/books.csv')   # Load existing books

        # Validate incoming data
        if not all(key in add_book for key in ("Title", "Author", "Genre", "Height", "Publisher")):
            return jsonify({'error': 'Missing required fields'}), 400

        for book in books_data:
            if (book["Title"] == add_book["Title"] and
                    book["Author"] == add_book["Author"] and
                    book["Genre"] == add_book["Genre"] and
                    book["Height"] == add_book["Height"] and
                    book["Publisher"] == add_book["Publisher"]):
                return jsonify({"error": "Book already existing"}), 400

        books_data.append(add_book)
        # updating csv file
        csv_path = os.path.join(os.path.dirname(__file__), 'data/books.csv')
        with open(csv_path, mode='a', encoding='utf-8', newline='') as csv_file:
            writer = csv.DictWriter(csv_file, fieldnames=["Title", "Author", "Genre", "Height", "Publisher"])
            writer.writerow(add_book)  # Append new book

        return jsonify({'books': books_data}), 201
        #return jsonify({'books': add_book}), 201

    except Exception as e:
        print(f"Errore del server: {str(e)}")
        return jsonify({"error": str(e)}), 500

#
# API PER ELIMINARE UN LIBRO
#
@app.route('/api/books', methods=['DELETE'])
def api_remove_book():
    try:
        books_data = load_csv_data('data/books.csv')
        remove_book = request.get_json()

        removed = False
        updated_books = []

        for book in books_data:
            if (book["Title"] == remove_book["Title"] and
                    book["Author"] == remove_book["Author"] and
                    book["Genre"] == remove_book["Genre"] and
                    book["Height"] == remove_book["Height"] and
                    book["Publisher"] == remove_book["Publisher"]):
                removed = True  # Libro trovato e rimosso
            else:
                updated_books.append(book)  # Mantieni i libri non rimossi

        if removed:
            csv_path = os.path.join(os.path.dirname(__file__), 'data/books.csv')

            with open(csv_path, mode="w", encoding="utf-8", newline="") as csv_file:
                fieldnames = ["Title", "Author", "Genre", "Height", "Publisher"]
                writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
                writer.writeheader()
                writer.writerows(updated_books)

            return jsonify({'books': updated_books}), 201 # per tabelle dinamiche con ajax
            #return jsonify({"success": "Book removed successfully"}), 200
            #se usiamo tabelle statiche che vanno ricaricate
        else:
            print("Libro non trovato per la rimozione.")
            return jsonify({"error": "Book not found"}), 404

    except Exception as e:
        print(f"Errore del server: {str(e)}")
        return jsonify({"error": str(e)}), 500

#
# FUNZIONE PYTHON PER VERIFICARE CHE I CAMPI
# DI UN FORMAT ABBIANO LE GIUSGTE CARATTERISTICHE
#

# GET mostra qualcosa così com'è
# POST modifica una risorsa
@app.route('/register', methods=['GET', 'POST'])
def register():
    errors = []
    if request.method == 'POST':
        name = request.form.get('username', '').strip()
        email = request.form.get('email', '').strip()
        password = request.form.get('password', '').strip()

        # Validazione campi
        if not name or not email or not password:
            return "Tutti i campi devono essere compilati."

        if not name.isalpha():
            return "Il nome deve contenere solo lettere."

        if len(password) < 8 or password.islower() or password.isalpha() or password.isdigit():
             return "La password deve avere almeno 8 caratteri, una maiuscola, una minuscola e un numero."

        if "@" not in email or "." not in email:
            return "Inserisci un'email valida."

        if not errors:
            return "Registrazione completata con successo!"

if __name__ == '__main__':
    app.run(debug=True)