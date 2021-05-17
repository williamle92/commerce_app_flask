from typing import Text
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, validators
from wtforms.fields.html5 import TelField
from wtforms.validators import DataRequired, EqualTo, Email, InputRequired, Length


class SignUpForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min= 2, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_pass = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField()

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField()


class DeleteForm(FlaskForm):
    submit = SubmitField


class UserInfoForm(FlaskForm):
    username = StringField('Username', validators=[InputRequired()])
    firstname = StringField('Firstname' , validators=[DataRequired()])
    lastname = StringField('Lastname' , validators=[DataRequired()])
    email = StringField('Email' , validators=[DataRequired(), Email()])
    address = StringField('Address', validators=[DataRequired()])
    phonenumber = TelField('Phonenumber' , validators=[InputRequired()])
    submit = SubmitField()

class InforForm(FlaskForm):
    name = StringField('Name', validators = [DataRequired()])
    address = StringField('Address', validators = [DataRequired()])
    city = StringField('City', validators = [DataRequired()])
    zipcode = StringField('Postcode', validators = [DataRequired()])
    phone = StringField('Phone', validators = [DataRequired()])
    submit = SubmitField()