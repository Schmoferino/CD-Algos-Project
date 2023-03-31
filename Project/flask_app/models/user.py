from flask_app import app
from flask import flash
from flask_app.config.mysqlconnection import connectToMySQL
from flask_bcrypt import Bcrypt
import re

bcrypt = Bcrypt(app)
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$') 

class User:
    def __init__(self, data):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.user_password = data['user_password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        
        self.posts = []

    @classmethod
    def users(cls):
        query = "SELECT * FROM users;"
        result = connectToMySQL('mydb').query_db(query)

        all_users = []
        for u in result:
            all_users.append(u)
        return all_users

    @classmethod
    def user_by_email(cls, data):
        query = "SELECT * FROM users WHERE users.email = %(login_email)s;"
        result = connectToMySQL('mydb').query_db(query, data)
        if not result:
            print('email not found -----')
            return False
        return cls(result[0])

    @classmethod
    def user_by_id(cls, data):
        query = "SELECT * FROM users WHERE users.id = %(id)s;"
        result = connectToMySQL('mydb').query_db(query, data)
        if not result:
            print("id not found -----")
            return False
        return cls(result[0])
    
    @classmethod
    def user_by_password(cls, data):
        query = "SELECT * FROM users WHERE users.user_password = %(user_password)s;"
        result = connectToMySQL('mydb').query_db(query, data)
        if not result:
            return False
        return cls(result[0])
    
    @classmethod
    def user_orders(cls, data):
        query = "SELECT * FROM orders JOIN users ON users.id = orders.user_id WHERE magazines.user_id = %(user_id)s;"
        result = connectToMySQL('mydb').query_db(query, data)

        user_orders = []
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

            poster = User(poster_info)
            one_order.poster = poster

            user_orders.append(one_order)
        return user_orders

    @classmethod
    def save_user(cls, data):
        query = "INSERT INTO users (first_name, last_name, email, user_password) VALUES ( %(first_name)s, %(last_name)s, %(email)s, %(user_password)s);"
        result = connectToMySQL('mydb').query_db(query, data)
        return result
    
    @classmethod
    def edit_user(cls, data):
        query = "UPDATE users SET first_name = %(first_name)s, last_name = %(last_name)s, email = %(email)s WHERE users.id = %(id)s"
        result = connectToMySQL('mydb').query_db(query, data)
        return result
    
    @staticmethod
    def isValid_register(user):
        is_valid = True
        if len(user['first_name']) < 3 or len(user['first_name']) > 20:
            flash("First name must have between 2 and 20 characters")
            is_valid = False
        if len(user['last_name']) < 3 or len(user['last_name']) > 20:
            flash("Last name must have between 2 and 20 characters")
            is_valid = False
        if not EMAIL_REGEX.match(user['email']): 
            flash("Invalid email address")
            is_valid = False
        return is_valid
    
    @staticmethod
    def isValid_login(user):
        is_valid = True
        if not User.user_by_email(user['login_email']):
            flash('Invalid email/password')
            is_valid = False
        if not User.user_by_password(user['login_password']):
            flash('Invalid email/password')
            is_valid = False
        return is_valid

    @staticmethod
    def isValid_update(user):
        is_valid = True
        if len(user['first_name']) < 3 or len(user['first_name']) > 20:
            flash("First name must have between 2 and 20 characters")
            is_valid = False
        if len(user['last_name']) < 3 or len(user['last_name']) > 20:
            flash("Last name must have between 2 and 20 characters")
            is_valid = False
        if not EMAIL_REGEX.match(user['email']): 
            flash("Invalid email address")
            is_valid = False
        return is_valid