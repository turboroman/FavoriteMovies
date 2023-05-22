from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Length


class AddForm(FlaskForm):
    title = StringField('Movie title',
                        validators=[DataRequired(), Length(max=50)])
    submit_btn = SubmitField('Add Movie')
