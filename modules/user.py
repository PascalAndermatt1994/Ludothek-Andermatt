from flask import Blueprint, flash, redirect, render_template, url_for
from flask_login import login_required, login_user, logout_user

from db.db import db
from forms.UserLoginForm import UserLoginForm
from forms.UserSignupForm import UserSignupForm
from models.user import User

from flask_bcrypt import Bcrypt
bcrypt = Bcrypt()

user_bp = Blueprint('user', __name__)

@user_bp.route('/', methods=['GET'])
@user_bp.route('/login', methods=['GET'])
def login():
  user_login_form = UserLoginForm()
  return render_template('user/login.html', form=user_login_form)

@user_bp.route('/login', methods=['POST'])
def login_post():
  user_login_form = UserLoginForm()
  if not user_login_form.validate():
    return redirect(url_for('user.login'))
  
  user = db.session.execute(db.select(User).filter_by(email=user_login_form.email.data)).scalar_one_or_none()
  if user is None:
    flash('Invalid email or password')
    return redirect(url_for('user.login'))
  else:
    login_user(user, remember=user_login_form.remember_me.data)
    return redirect(url_for('home.index'))
      
@user_bp.route('/logout', methods=['GET'])
@login_required
def logout():
  logout_user()
  return redirect(url_for('user.login'))

@user_bp.route('/signup', methods=['GET'])
def signup():
  user_signup_form = UserSignupForm()
  return render_template('user/signup.html', form=user_signup_form)

@user_bp.route('/signup', methods=['POST'])
def signup_post():
  user_signup_form = UserSignupForm()
  if not user_signup_form.validate():
    return redirect(url_for('user.signup'))

  user = db.session.execute(db.select(User).filter_by(email=user_signup_form.email.data)).scalar_one_or_none()
  if user is not None:
    flash('Email address already exists')
    return redirect(url_for('user.signup'))

  new_user = User(email=user_signup_form.email.data, name=user_signup_form.name.data, password=bcrypt.generate_password_hash(user_signup_form.password.data).decode('utf-8'))
  
  db.session.add(new_user)
  db.session.commit()
  
  return redirect(url_for('user.login'))