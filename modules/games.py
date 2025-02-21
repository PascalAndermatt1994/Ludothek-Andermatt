from flask import Blueprint, render_template, redirect, url_for, flash
from flask_login import login_required, current_user
from models.games import games
from forms.games.GamesForm import GamesForm
from db.db import db
from datetime import datetime

games_bp = Blueprint('games', __name__)

@games_bp.route('/', methods=['GET'])
@games_bp.route('/index', methods=['GET'])
@login_required
def index():
    all_games = games.query.order_by(games.gamenames).all()
    return render_template('index.html', games=all_games)

@games_bp.route('/add', methods=['GET', 'POST'])
@login_required
def add_game():
    form = GamesForm()
    if form.validate_on_submit():
        new_game = games(
            gamenames=form.gamenames.data,
            description=form.description.data,
            playernumber=form.playernumber.data,
            status=form.status.data,
            user_id=current_user.id
        )
        db.session.add(new_game)
        db.session.commit()
        flash('Game added successfully!', 'success')
        return redirect(url_for('games.index'))
    return render_template('games/add.html', form=form)

@games_bp.route('/edit/<int:game_id>', methods=['GET', 'POST'])
@login_required
def edit_game(game_id):
    game = games.query.get_or_404(game_id)
    form = GamesForm(obj=game)
    if form.validate_on_submit():
        game.gamenames = form.gamenames.data
        game.description = form.description.data
        game.playernumber = form.playernumber.data
        game.status = form.status.data
        db.session.commit()
        flash('Game updated successfully!', 'success')
        return redirect(url_for('games.index'))
    return render_template('games/edit.html', form=form, game=game)

@games_bp.route('/delete/<int:game_id>', methods=['POST'])
@login_required
def delete_game(game_id):
    game = games.query.get_or_404(game_id)
    db.session.delete(game)
    db.session.commit()
    flash('Game deleted successfully!', 'success')
    return redirect(url_for('games.index'))

@games_bp.route('/lend/<int:game_id>', methods=['POST'])
@login_required
def lend_game(game_id):
    game = games.query.get_or_404(game_id)
    if not game.is_lent:
        game.is_lent = True
        game.lent_at = datetime.utcnow()
        db.session.commit()
        flash('Game lent successfully!', 'success')
    else:
        flash('Game is already lent!', 'danger')
    return redirect(url_for('games.index'))

@games_bp.route('/return/<int:game_id>', methods=['POST'])
@login_required
def return_game(game_id):
    game = games.query.get_or_404(game_id)
    if current_user.is_admin:
        if game.is_lent:
            game.is_lent = False
            game.lent_at = None
            db.session.commit()
            flash('Game returned successfully!', 'success')
        else:
            flash('Game is not currently lent!', 'danger')
    else:
        flash('You do not have permission to return games!', 'danger')
    return redirect(url_for('games.index'))