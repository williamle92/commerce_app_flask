from flask import render_template, request, redirect, url_for, flash
from flask_login.utils import login_required
from app.forms import DeleteForm, SignUpForm, UserInfoForm, LoginForm 

from flask_wtf.file import FileField, FileRequired
from flask_wtf.form import FlaskForm
from werkzeug.utils import secure_filename
from werkzeug.security import check_password_hash
from werkzeug.urls import url_parse
from wtforms import validators
from flask_login import current_user, login_user, logout_user, UserMixin, login_required
from app.models import User, Cart
from app import app, db, mail
from flask_mail import Message


@app.route('/')
@app.route('/index')
def index():
    title= 'Home'

    return render_template('index.html')
