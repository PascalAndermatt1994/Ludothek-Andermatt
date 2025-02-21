import logging
from flask import Blueprint, jsonify, make_response, request
from flask_jwt_extended import jwt_required, create_access_token
from models.games import games
from models.user import User
from db.db import db
from werkzeug.security import check_password_hash, generate_password_hash

api_bp = Blueprint('api', __name__)

# Configure logging
logging.basicConfig(level=logging.DEBUG)

@api_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    logging.debug(f"Login data received: {data}")
    user = User.query.filter_by(email=data['email']).first()
    if user:
        logging.debug(f"User found: {user}")
        logging.debug(f"Stored password hash: {user.password}")
        logging.debug(f"Password provided: {data['password']}")
        try:
            if check_password_hash(user.password, data['password']):
                access_token = create_access_token(identity=user.id)
                logging.debug(f"Access token generated: {access_token}")
                return make_response(jsonify(access_token=access_token), 200)
            else:
                logging.debug("Invalid password")
        except ValueError as e:
            logging.error(f"Password hash error: {e}")
    else:
        logging.debug("User not found")
    return make_response(jsonify(message="Invalid credentials"), 401)

@api_bp.route('/games', methods=['GET'])
@jwt_required()
def get_games():
    all_games = games.query.all()
    games_list = [{"id": game.id, "gamenames": game.gamenames, "description": game.description, "playernumber": game.playernumber, "status": game.status, "is_lent": game.is_lent} for game in all_games]
    return make_response(jsonify(data=games_list), 200)

@api_bp.route('/games/<int:game_id>', methods=['GET'])
@jwt_required()
def get_game(game_id):
    game = games.query.get_or_404(game_id)
    game_data = {"id": game.id, "gamenames": game.gamenames, "description": game.description, "playernumber": game.playernumber, "status": game.status, "is_lent": game.is_lent}
    return make_response(jsonify(data=game_data), 200)

@api_bp.route('/games', methods=['POST'])
@jwt_required()
def add_game():
    data = request.get_json()
    new_game = games(
        gamenames=data['gamenames'],
        description=data['description'],
        playernumber=data['playernumber'],
        status=data['status']
    )
    db.session.add(new_game)
    db.session.commit()
    return make_response(jsonify(message="Game added successfully!"), 201)

@api_bp.route('/games/<int:game_id>', methods=['PUT'])
@jwt_required()
def update_game(game_id):
    data = request.get_json()
    game = games.query.get_or_404(game_id)
    game.gamenames = data['gamenames']
    game.description = data['description']
    game.playernumber = data['playernumber']
    game.status = data['status']
    db.session.commit()
    return make_response(jsonify(message="Game updated successfully!"), 200)

@api_bp.route('/games/<int:game_id>', methods=['DELETE'])
@jwt_required()
def delete_game(game_id):
    game = games.query.get_or_404(game_id)
    db.session.delete(game)
    db.session.commit()
    return make_response(jsonify(message="Game deleted successfully!"), 200)
