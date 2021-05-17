from flask import render_template, request, redirect, url_for, flash, session
from flask_login.utils import login_required
from app.forms import DeleteForm, InforForm, SignUpForm, UserInfoForm, LoginForm 
from flask_wtf.file import FileField, FileRequired
from flask_wtf.form import FlaskForm
from werkzeug.utils import secure_filename
from werkzeug.security import check_password_hash
from werkzeug.urls import url_parse
from wtforms import validators
from flask_login import current_user, login_user, logout_user, UserMixin, login_required
from app.models import *
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

    return render_template('login.html', title=title, form=form, current_user=current_user)

@app.route('/logout')
def logout():
    logout_user()
    flash('You have successfully logged out!', 'primary')
    return redirect(url_for('login'))


@app.route('/viewitem')
@login_required
def viewitem(itemid):
    items= Item.query.get_or_404(itemid)
    title = 'View Item'
    return render_template('viewitem.html', items=items, title=title)


@app.route('/cart', methods=['POST','GET'])
def cart():
    subtotal = 0
    order = {}
    session['quantity'] = 0
    productc = Item()
    if 'cart' in session:
        print(session['cart'])
        for d in session['cart']:
            for k in d:
                product = Item.query.filter_by(title = k).first()
                order[product.title] = []
                order[product.title].append(productc.price) 
                order[product.title].append(productc.image_file) 
                order[product.title].append(d[k])
                order[product.title].append(productc.price * d[k]) 
                subtotal += productc.price * d[k]
                session['quantity'] += d[k]
    print(order)   
    session['order'] = order
    print('You have your own items!')
    shipping = 10
    total = subtotal + shipping
    session['shipping'] = shipping
    session['subtotal'] = subtotal
    session['total'] = total
    return render_template('cart.html', title = 'Cart', total = total, subtotal = subtotal, shipping = shipping, order = order)



@app.route('/items/<int:item_id>', methods=['POST','GET'])
def additem(item_id):
    products = Item()
    item = Item.query.get_or_404(item_id)
    print("product", item.title)
    if request.method == 'POST':
        quantity = int(request.form.get('quantity'))
        if "cart" in session:
            if not any(item.title in d for d in session['cart']):
                session['cart'].append({item.title: quantity})  
            elif any(item.title in d for d in session['cart']):
                for d in session['cart']:
                    if item.title in d:
                        d[item.title] += quantity
        else:
            session['cart'] = [{item.title: quantity}]
        print(session['cart'])
        session['quantity'] = 0
        for k in session['cart']:
            for d in k:
                session['quantity'] += k[d]
   
        flash(f'Adding to shopping cart succesfully!', 'success')
    
    return render_template('viewitem.html', title = 'Product', item = item)


@app.route('/cart/update',methods=['POST'])
def update_cart():
    qty = request.form.get('update_qty')
    p = request.form.get('update_p')
    print(p,qty)
    print("update_cart")
    for i in session['cart']:
        if p in i:
            i.update({p:int(qty)})
    print(session['cart'])
    return redirect(url_for('cart'))

@app.route('/cart/remove/<string:product_title>', methods=['POST'])
def remove_from_cart(product_title):
    print('before', session['cart'])
    for i in session['cart']:
        if product_title in i:
            i.pop(product_title)
    print('after', session['cart'])
    return redirect(url_for('cart'))

@app.route('/cart/deleteall', methods=['POST'])
def delete_all():
    session.pop('cart')
    return redirect(url_for('cart'))



@app.route('/checkout', methods=['GET','POST'])
def checkout():
    total = session['total']
    subtotal = session['subtotal']
    shipping = session['shipping']
    form = InforForm()
    if form.validate_on_submit():
        country = request.form.get('country_select')
        infor = InforForm(name = form.name.data, address = form.address.data, country = country, city = form.city.data, zipcode = form.zipcode.data, phone = form.phone.data, total_price = total)
        db.session.add(infor)
        db.session.commit()
        item = []
        if 'order' in session:
            for k in session['order']:
                product = Item.query.filter_by(title = k).first()
                c1 = Cart(product_id = product.id, quantity = session['order'][k][2])
                item.append(c1)
        infor.cart.extend(item)
        db.session.add_all(item)
        db.session.commit()
        flash(f'You ordered successully!', 'success')
        session.pop('cart')
        session.pop('order')
        return redirect(url_for('index'))
    return render_template('checkout.html', title = 'Check Out', form = form, total = total, subtotal = subtotal, shipping = shipping)