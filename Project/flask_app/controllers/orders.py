from flask_app import app
from flask import render_template, redirect, request, session, flash
from flask_app.models.user import User
from flask_app.models.order import Order

@app.route('/carp_services/main')
def main():
    if session['login'] == False:
        flash('Login to continue')
        return redirect('/carp_services/signup')
    orders = Order.order_by_soonest()
    print(orders)
    data = {
        'id': session['id']
    }
    user = User.user_by_id(data)
    updates = Order.all_updates()
    return render_template('main.html', orders = orders, user = user, updates = updates)

@app.route('/carp_services/schedule')
def schedule():
    data = {
        'id': session['id']
    }
    user = User.user_by_id(data)
    orders = Order.order_by_soonest()
    return render_template('schedule.html',  orders = orders, user = user)

@app.route('/carp_services/zones')
def zones():
    data = {
        'id': session['id']
    }
    user = User.user_by_id(data)
    return render_template('zones.html', user = user)

@app.route('/carp_services/updates')
def service_updates():
    updates = Order.all_updates()
    data = {
        'id': session['id']
    }
    user = User.user_by_id(data)
    return render_template('updates.html', user = user, updates = updates)

@app.route('/carp_services/new_order')
def new_order():
    data = {
        'id': session['id']
    }
    user = User.user_by_id(data)
    schedules = Order.all_orders()
    return render_template('new.html', user = user, schedules = schedules)

@app.route('/carp_services/post_order')
def post():
    schedules = Order.all_orders()
    data = {
        'user_id': session['id'],
        'order_type': request.form['order_type'],
        'order_date': request.form['order_date'],
        'order_desc': request.form['order_desc']
    }
    for i in schedules:
        if request.form['order_date'] in i:
            flash('Must use an available date')
            return redirect('/carp_services/new_order')
    if not Order.validate_order(data):
        return redirect('/carp_services/new_order')
    Order.save_order(data)
    flash("Posted " + request.form['order_type'] + " !")
    return redirect('/carp_services/schedule')
