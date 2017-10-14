from flask_wtf import FlaskForm
from wtforms import BooleanField, StringField
from wtforms.validators import DataRequired


class SearchForm(FlaskForm):
    search = StringField(
        'search',
        validators=[DataRequired()]
    )
