from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, DecimalField
from wtforms.validators import DataRequired, Length


class UpdateForm(FlaskForm):
    new_rating = DecimalField('New rating: ',
                              validators=[DataRequired()])
    new_review = StringField('New review: ',
                             validators=[DataRequired(), Length(max=300)])
    submit_btn = SubmitField('Done')
