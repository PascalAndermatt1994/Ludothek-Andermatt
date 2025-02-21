import logging
from flask import Blueprint, jsonify, make_response, request
from flask_jwt_extended import jwt_required, create_access_token
from models.games import games
from models.user import User
from db.db import db
from flask_bcrypt import Bcrypt

api_bp = Blueprint('api', __name__)
bcrypt = Bcrypt()

@api_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    user: User = User.query.filter_by(email=data['email']).first()
    if user and bcrypt.check_password_hash(user.password, data['password']):
        access_token = create_access_token(identity=user.email)
        return make_response(jsonify(access_token=access_token), 200)
    return make_response(jsonify(message="Invalid credentials"), 401)

@api_bp.route('/games', methods=['GET'])
@jwt_required()
def get_games():
    all_games = games.query.all()
    return make_response(jsonify(data=all_games), 200)

@api_bp.route('/games/<int:game_id>', methods=['GET'])
@jwt_required()
def get_game(game_id):
    game = games.query.get_or_404(game_id)
    return make_response(jsonify(data=game), 200)

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
