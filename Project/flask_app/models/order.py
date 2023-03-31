from flask_app import app
from flask import flash
from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.models import user
import datetime
class Order:
    def __init__(self, data):
        self.order_id = data['order_id']
        self.user_id = data['user_id']
        self.order_type = data['order_type']
        self.order_date = data['order_date']
        self.order_desc = data['order_desc']
        self.created_at = data['created_at']
        self.updated_at = data['created_at']

        self.poster = None

    @classmethod
    def all_orders(cls):
        query = "SELECT * FROM orders JOIN users ON users.id = orders.user_id;"
        result = connectToMySQL('mydb').query_db(query)

        orders = []
        for i in result:
            one_order = cls(i)

            poster_info = {
                'id': i['id'],
                'first_name': i['first_name'],
                'last_name': i['last_name'],
                'email': i['email'],
                'user_password': i['user_password'],
                'created_at': i['created_at'],
                'updated_at': i['updated_at']
            }

            poster = user.User(poster_info)
            one_order.poster = poster

            orders.append(one_order)
        return orders
    
    @classmethod
    def order_by_id(cls, data):
        query = "SELECT * FROM orders JOIN users ON users.id = orders.user_id WHERE orders.order_id = %(order_id)s;"
        result = connectToMySQL('mydb').query_db(query, data)
        one_order = cls(result[0])

        poster_info = {
                'id': result[0]['user_id'],
                'first_name': result[0]['first_name'],
                'last_name': result[0]['last_name'],
                'email': result[0]['email'],
                'user_password': result[0]['user_password'],
                'created_at': result[0]['users.created_at'],
                'updated_at': result[0]['users.updated_at']
        }

        poster = user.User(poster_info)
        one_order.poster = poster
        return one_order
    
    @classmethod
    def order_by_soonest(cls):
        query = "SELECT * FROM orders JOIN users ON users.id = orders.user_id WHERE orders.order_date > NOW() ORDER BY orders.order_date ASC;"
        result = connectToMySQL('mydb').query_db(query)
        return result
    
    @classmethod
    def user_orders(cls, data):
        query = "SELECT * FROM orders JOIN users ON users.id = orders.user_id WHERE orders.user_id = %(user_id)s;"
        result = connectToMySQL('mydb').query_db(query, data)

        orders = []
        for i in result:
            one_order = cls(i)

            poster_info = {
                'id': i['id'],
                'first_name': i['first_name'],
                'last_name': i['last_name'],
                'email': i['email'],
                'user_password': i['user_password'],
                'created_at': i['created_at'],
                'updated_at': i['updated_at']
            }

            poster = user.User(poster_info)
            one_order.poster = poster

            orders.append(one_order)
        return orders
    
    @classmethod
    def save_order(cls, data):
        query = "INSERT INTO orders ( order_type, order_date, order_desc ) VALUES ( %(order_type)s, %(order_date)s, %(order_desc)s);"
        result = connectToMySQL('mydb').query_db(query, data)
        return result
    
    @classmethod
    def delete_order(cls, data):
        query = "DELETE FROM orders WHERE order_id = %(order_id)s;"
        result = connectToMySQL('mydb').query_db(query)
        return result
    
    @classmethod
    def all_updates(cls):
        query = "SELECT * FROM updates JOIN users ON users.id = updates.user_id ORDER BY updates.created_at DESC;"
        result = connectToMySQL('mydb').query_db(query)
        return result 
    
    #       In future editions of the site, image file hosting is planned to be implemented for update posts. 
    #       That will likely require a new controller and model for its own data processing.
    
    @staticmethod
    def isValid_order(order):
        is_valid = True
        if order['order_date'] < (datetime.date.now() + datetime.timedelta(weeks = 1)) or order['order_date'] > (datetime.date.now() + datetime.timedelta(months = 2)):
            flash("'Date must be within a week from and under two months from today'")
            is_valid = False
        if len(order['order_description']) < 20 or len(order['order_description']) > 512:
            flash('Description must have between 20 and 512 characters')
            is_valid = False
        return is_valid