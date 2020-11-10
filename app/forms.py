from flask_wtf import FlaskForm
from wtforms import IntegerField, StringField, SubmitField, validators


class StartUpForm(FlaskForm):
    denom_1 = IntegerField(' R1 coins', [validators.DataRequired()])
    denom_2 = IntegerField(' R2 coins', [validators.DataRequired()])
    denom_3 = IntegerField(' R5 coins', [validators.DataRequired()])
    denom_4 = IntegerField(' R10 coins(note)', [validators.DataRequired()])
    items_filename = StringField(' Items data filename', [
                                 validators.DataRequired()])
    submit = SubmitField('Start vending machine')


class UpdateWallet(FlaskForm):
    denom_1 = IntegerField(' R1 coins', [validators.DataRequired()])
    denom_2 = IntegerField(' R2 coins', [validators.DataRequired()])
    denom_3 = IntegerField(' R5 coins', [validators.DataRequired()])
    denom_4 = IntegerField(' R10 coins(note)', [validators.DataRequired()])
    submit = SubmitField('Update Wallet')


class UpdateItems(FlaskForm):
    items_filename = StringField('Items data filename', [
                                 validators.DataRequired()])
    submit = SubmitField('Update Items')


class BuyForm(FlaskForm):
    denom_1 = IntegerField(' R1 coins', [validators.DataRequired()])
    denom_2 = IntegerField(' R2 coins', [validators.DataRequired()])
    denom_3 = IntegerField(' R5 coins', [validators.DataRequired()])
    denom_4 = IntegerField(' R10 coins(note)', [validators.DataRequired()])
    item_name = StringField('Item name', [validators.DataRequired()])
    submit = SubmitField('Buy item')
