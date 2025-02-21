from flask_wtf import FlaskForm
from wtforms import EmailField, PasswordField, StringField
from wtforms.validators import DataRequired, Email
from models.user import User
from db.db import db

class UserSignupForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    email = EmailField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])

    def create_user(self):
        user = User(
            name=self.name.data,
            email=self.email.data
        )
        user.set_password(self.password.data)
        db.session.add(user)
        db.session.commit()
        return user