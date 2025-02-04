# se clicchiamo sul sito dei link, vediamo su terminale le GET
# e le rischieste con i rispettivi codici

from flask import Flask, render_template, request, jsonify
import csv
import os.path

# load team members from csv

def load_team_data():
    team_members = []
    csv_path = os.path.join(os.path.dirname(__file__), 'static/team.csv')
    try:
        with open(csv_path, mode='r', encoding='utf-8') as csv_file:
            csv_reader = csv.DictReader(csv_file)
            for row in csv_reader:
                team_members.append(row)
            return team_members
    except FileNotFoundError:
        print(f"Warning: {csv_path} not found!")
        return []
    except Exception as e:
        print(f"Warning: {csv_path} not found!")
        return []

# load books data from csv

def load_books_data():
    books_data = []
    csv_path = os.path.join(os.path.dirname(__file__), 'static/books.csv')
    try:
        with open(csv_path, mode='r', encoding='utf-8') as csv_file:
            csv_reader = csv.DictReader(csv_file)
            for row in csv_reader:
                books_data.append(row)
            return books_data
    except FileNotFoundError:
        print(f"Warning: {csv_path} not found!")
        return []
    except Exception as e:
        print(f"Warning: {csv_path} not found!")
        return []

def load_products_data():
    products_data = []
    csv_path = os.path.join(os.path.dirname(__file__), 'static/products.csv')
    try:
        with open(csv_path, mode='r', encoding='utf-8') as csv_file:
            csv_reader = csv.DictReader(csv_file)
            for row in csv_reader:
                products_data.append(row)
            return products_data
    except FileNotFoundError:
        print(f"Warning: {csv_path} not found!")
        return []
    except Exception as e:
        print(f"Warning: {csv_path} not found!")
        return []
app = Flask(__name__)
@app.route('/') #home page
def index():
    products_data = load_products_data()
    return render_template('index.html', products_data=products_data)

@app.route('/contact')
def contact():
    return render_template('contact.html')

@app.route('/team')
def team():
    team_members = load_team_data()
    return render_template('team.html', team_members=team_members)

@app.route('/about') # contains also the books list
def about():
    books_data = load_books_data()
    return render_template('about.html', books_data=books_data)



@app.route('/api/books', methods=['GET'])
def api_books():
    books_data = load_books_data()
    return jsonify(books_data)


# API per cercare un libro dal titolo o l'autore
@app.route('/api/books/search', methods=['GET'])
def search_books():
    try:
        title_query = request.args.get('title', '').strip().lower()
        author_query = request.args.get('author', '').strip().lower()

        # Carica i dati dal CSV
        books = load_books_data()

        # Filtra i libri in base al titolo o all'autore
        filtered_books = [
            book for book in books
            if (title_query in book["Title"].strip().lower() if title_query else True) and
               (author_query in book["Author"].strip().lower() if author_query else True)
        ]

        return jsonify({"books": filtered_books}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500


# API per aggiungere un libro con controllo dei doppioni
@app.route('/api/books', methods=['POST'])
def add_book_api():
    try:
        add_book = request.get_json()  # Get data from the request
        books_data = load_books_data()      # Load existing books

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
        csv_path = os.path.join(os.path.dirname(__file__), 'static/books.csv')
        with open(csv_path, mode='a', encoding='utf-8', newline='') as csv_file:
            writer = csv.DictWriter(csv_file, fieldnames=["Title", "Author", "Genre", "Height", "Publisher"])
            writer.writerow(add_book)  # Append new book

        return jsonify({'message': 'Book added successfully', 'book': add_book}), 201

    except Exception as e:
        return jsonify({'error': f'An error: {str(e)}'}), 500


# API to delete an existing book
@app.route('/api/books', methods=['DELETE'])
def api_remove_book():
    try:
        books_data = load_books_data()
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
            csv_path = os.path.join(os.path.dirname(__file__), 'static/books.csv')

            with open(csv_path, mode="w", encoding="utf-8", newline="") as csv_file:
                fieldnames = ["Title", "Author", "Genre", "Height", "Publisher"]
                writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
                writer.writeheader()
                writer.writerows(updated_books)

            return jsonify({"success": "Book removed successfully"}), 200
        else:
            print("Libro non trovato per la rimozione.")
            return jsonify({"error": "Book not found"}), 404

    except Exception as e:
        print(f"Errore del server: {str(e)}")
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)