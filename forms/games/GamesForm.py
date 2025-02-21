from flask_wtf import FlaskForm
from wtforms import StringField, BooleanField, SubmitField
from wtforms.validators import DataRequired, Length

class GamesForm(FlaskForm):
    gamenames = StringField('Game Name', validators=[DataRequired(), Length(max=256)])
    description = StringField('Description', validators=[DataRequired(), Length(max=4096)])
    playernumber = StringField('Number of Players', validators=[DataRequired(), Length(max=10)])
    status = BooleanField('Status')
    submit = SubmitField('Submit')
