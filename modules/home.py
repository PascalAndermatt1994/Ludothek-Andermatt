from flask import Blueprint, render_template
from flask_login import login_required

from models.games import games

home_bp = Blueprint('home', __name__)

@home_bp.route('/', methods=['GET'])
@home_bp.route('/index', methods=['GET'])
@login_required
def index():
  Game = games.query.order_by(games.gamenames).all()
  return render_template('index.html', games=Game)