from werkzeug.utils import redirect
from flask_app import app
from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.controllers import user_controller
from flask import flash
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)

import re	
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$') 

class User:
    def __init__( self, data ):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.password = data['password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
    
    @staticmethod
    def register_validation(form_data):
        is_valid = True
        if len(form_data['first_name']) < 2:
            flash('First name must be at least two characters')
            is_valid = False
        if len(form_data['last_name']) < 2:
            flash('Last name must be at least two characters')
            is_valid = False
        if len(form_data['password']) < 8:
            flash('Password must be at least eight characters')
            is_valid = False
        if not form_data['password'] == form_data['conf_pass']:
            flash('Password and confirmation password must be identical')
            is_valid = False
        if not EMAIL_REGEX.match(form_data['email']):
            flash("Email needs to be formatted in valid fashion")
            is_valid = False
        return is_valid
    
    @staticmethod
    def login_validation(validation_data):
        is_valid=True
        if not validation_data['user']:
            flash('Invalid Email/Password')
            is_valid = False
        elif not bcrypt.check_password_hash(validation_data['user'].password, validation_data['password']):
            flash("Invalid Email/Password")
            is_valid = False
        return is_valid

    @classmethod
    def register_user(cls, data):
        query = 'INSERT INTO users (first_name, last_name, email, password, created_at, updated_at) VALUES (%(first_name)s, %(last_name)s, %(email)s, %(password)s, NOW(), NOW());'
        results = connectToMySQL('login_and_reg').query_db(query, data)
        return results

    @classmethod
    def get_by_email(cls, data):
        query = 'SELECT * FROM users WHERE email = %(email)s'
        result = connectToMySQL('login_and_reg').query_db(query, data)
        if len(result) < 1:
            return False
        return cls(result[0])
    
    @classmethod
    def get_user_info(cls, data):
        query = 'SELECT * FROM users WHERE id = %(user_id)s'
        result = connectToMySQL('login_and_reg').query_db(query, data)
        return cls(result[0])