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
@login_required
def index():
    title= 'Home'

    return render_template('index.html', title=title)


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    title='Sign Up'
    form = SignUpForm()
    if request.method == 'POST' and form.validate_on_submit():
        username = form.username.data
        email = form.email.data
        password = form.password.data

        existing_user = User.query.filter((User.username == username) | (User.email == email)).all()
        if existing_user:
            flash('The email or username is already in use. Please try again.', 'danger')
            return redirect(url_for("signup"))

        newuser = User(username, email, password)
        db.session.add(newuser)
        db.session.commit()
        flash(f"Thank you {username} for creating an account with us! We hope you enjoy your time here!", 'success')
        return redirect(url_for('login'))
    return render_template('signup.html', title=title, form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    title='Login'
    form = LoginForm()
    if request.method == 'POST' and form.validate_on_submit():
        username = form.username.data
        password = form.password.data

        user= User.query.filter_by(username=username).first()
        if user is None or not check_password_hash(user.password, password):
            flash('That is an invalid username or password! Please try again.' , 'danger')
            return redirect(url_for('login'))
        
        login_user(user, remember=form.remember_me.data)
        flash('You have succesfully logged in!', 'success')
        return redirect(url_for('index'))
    return render_template('login.html', title=title, form=form)

 