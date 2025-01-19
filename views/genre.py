from models import db, Genre
from flask import Blueprint, jsonify, request


genre_bp = Blueprint("genre_bp", __name__)

# FETCH ALL GENRES
@genre_bp.route("/genres")
def fetch_genres():
    genres = Genre.query.all()
    genre_list = [{"id":genre.id, "name":genre.name} for genre in genres]
    return jsonify({"genres":genre_list})

# FETCH GENRE BY ID
@genre_bp.route("/genres/<int:genre_id>")
def fetch_genre(genre_id):
    genre = Genre.query.get(genre_id)
    if not genre:
        return jsonify({"error": "Genre not found"})
    return jsonify({"genre": {"id":genre.id, "name":genre.name}})

# CREATE GENRE
@genre_bp.route("/genres", methods=["POST"])
def add_genre():
    data = request.get_json()

    name = data['name']

    if not name:
        return jsonify({"error": "Name is required"})
    
    check_name = Genre.query.filter_by(name=name).first()

    if check_name:
        return jsonify({"error": "Genre already exists"})
    
    else:
        new_genre = Genre(name=name)
        db.session.add(new_genre)
        db.session.commit()
        return jsonify({"success": "Genre created successfully"})
    


# UPDATE GENRE
@genre_bp.route("/genres/<int:genre_id>", methods=["PATCH"])
def update_genre(genre_id):
    data = request.get_json()

    name = data.get("name")
    genre = Genre.query.get(genre_id)

    if not genre:
        return jsonify({"error": "Genre not found"})
    
    if name:
        existing_genre = Genre.query.filter_by(name=name).first()

        if existing_genre and existing_genre.id != genre_id:
            return jsonify({"error": "This genre already exists"})
        
        genre.name = name
        db.session.commit()
        return jsonify({"success": "Genre updated successfully"})
    
    return jsonify({"error": "Name of the genre is required"})




# DELETE GENRE
@genre_bp.route("/genres/<int:genre_id>", methods=["DELETE"])
def delete_genre(genre_id):
    genre = Genre.query.get(genre_id)

    if not genre:
        return jsonify({"error": "Genre not found"})
    
    db.session.delete(genre)
    db.session.commit()
    return jsonify({"success": "Genre deleted successfully"})


