from flask_wtf import FlaskForm
from wtforms import SelectField, TextAreaField, SubmitField
from wtforms.validators import DataRequired
from valid import BetterDecimalField


class TestForm(FlaskForm):
    amount = BetterDecimalField('Amount', validators=[DataRequired()], places=2, round_always=True)
    payway = SelectField('Payway', validators=[DataRequired()],
                         choices=[('USD', 'USD'), ('RUB', 'RUB'), ('EUR', 'EUR')])
    description = TextAreaField('Description')
    submit = SubmitField('Pay')