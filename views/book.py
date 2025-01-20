from models import db, Book, Genre, User
from flask import Blueprint, jsonify, request

book_bp = Blueprint("book_bp", __name__)

# ADD BOOK
@book_bp.route("/books", methods=["POST"])
def add_book():
    data = request.get_json()

    title = data['title']
    author = data['author']
    genre_id = data['genre_id']
    user_id = data['user_id']

    check_genre_id = Genre.query.get(genre_id)
    check_user_id = User.query.get(user_id)

    if not check_genre_id or not check_user_id:
        return jsonify({"error": "Invalid genre or user id"})
    
    else:
        new_book = Book(title=title, author=author, genre_id=genre_id, user_id=user_id)
        db.session.add(new_book)
        db.session.commit()
        return jsonify({"success": "Book added successfully"})
    

# FETCH ALL BOOKS
@book_bp.route("/books")
def fetch_books():
    books = Book.query.all()
    books_list=[]

    for book in books:
        books_list.append({
            "id": book.id,
            "title": book.title,
            "author": book.author,
            "genre_id": book.genre_id,
            "user_id": book.user_id
        })
    return jsonify({"books": books_list})

# FETCH BOOK BY ID
@book_bp.route("/books/<int:book_id>")
def fetch_book(book_id):
    book = Book.query.get(book_id)

    if book:
        return jsonify({
            "id": book.id,
            "title": book.title,
            "author": book.author,
            "genre_id": book.genre_id,
            "user_id": book.user_id
            })
    else:
        return jsonify({"error": "Book not found"})
    

# UPDATE BOOK   
@book_bp.route("/books/<int:book_id>", methods=["PATCH"])
def update_book(book_id):
    data = request.get_json()
    book = Book.query.get(book_id)

    if book:
        title = data.get('title', book.title)
        author = data.get('author', book.author)
        genre_id = data.get('genre_id', book.genre_id)
        user_id = data.get('user_id', book.user_id)

        check_book_id = Book.query.get(book_id)
        if not check_book_id:
            return jsonify({"error": "Book not found"})

        else:
            book.title = title
            book.author = author
            book.genre_id = genre_id
            book.user_id = user_id

            db.session.commit()
            return jsonify({"success": "Book updated successfully!!!"})

    else:
        return jsonify({"error": "Book not found"})


# DELETE BOOK
@book_bp.route("/books/<int:book_id>", methods=["DELETE"])
def delete_book(book_id):
    book = Book.query.filter_by(id = book_id, user_id = current_user.id).first()

    if not book:
        return jsonify({"error": "Book has not been found"})

    db.session.delete(book)
    db.session.commit()
    return jsonify({"success": "Book deleted successfully!!!"})

