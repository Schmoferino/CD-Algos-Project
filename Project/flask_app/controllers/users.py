from flask_app import app
from flask import render_template, redirect, request, session, flash
from flask_app.models.user import User
from flask_app.models.order import Order
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app) 

@app.route("/carp_services/signup")
def index():
    return render_template('index.html')

@app.route('/carp_services/register', methods=['POST'])
def register():
    if not request.form['user_password'] or not request.form['confirm_password']:
        flash('Password fields are empty')
        return redirect('/carp_services/signup')
    pw_hash = bcrypt.generate_password_hash(request.form['user_password'])
    data = {
        "first_name": request.form['first_name'],
        "last_name": request.form['last_name'],
        "email": request.form['email'],
        "user_password": pw_hash,
        "confirm_password": request.form['confirm_password']
    }

    if not User.isValid_register(data):
        return redirect('/carp_services/login')
    if request.form['user_password'] != request.form['confirm_password']:
        flash("Confirmation doesn't match password")
        return redirect('/carp_services/signup')
    if len(request.form['user_password']) < 8:
        flash('Password must be 8 or more characters')
        return redirect('/carp_services/signup')
    user = User.save_user(data)
    print(data)

    session['id'] = user['id']
    session['login'] = True
    return redirect('/carp_services/main')

@app.route('/carp_services/login', methods = ['POST'])
def login():
    data = {
        'login_email': request.form['login_email'],
        'user_password': bcrypt.generate_password_hash(request.form['login_password'])
    }
    check = User.user_by_email(data)
    print(check) 
    
    if not check:
        flash('Credentials not found')
        return redirect('/carp_services/login')
    if not bcrypt.check_password_hash(check.user_password, request.form['login_password']):
        flash('Credentials not found')
        print('BCRYPT')
        return redirect('/carp_services/login')
    session['id'] = check['id']
    session['login'] = True
    return redirect('/carp_services/main')


@app.route('/carp_services/account')
def view_user():
    data = {
        'user_id': session['id'],
    }
    user = User.user_by_id(data)
    order = Order.user_orders(data)
    return render_template('account.html', user = user, order = order)

@app.route('/carp_services/update')
def update():
    data = {
        "id": session['id'],
        "first_name": request.form['first_name'],
        "last_name": request.form['last_name'],
        "email": request.form['email']
    }
    if not User.isValid_update(data):
        return redirect('/carp_services/account')
    User.edit_user(data)
    return redirect('/carp_services/account')

@app.route('/carp_services/logout')
def logout():
    session['id'] = None
    session['login'] = False
    return redirect('/carp_services/signup')