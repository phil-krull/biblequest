from biblequest.config.mysqlconnection import connectToMySQL
from flask import request

from biblequest import app
from flask_bcrypt import Bcrypt

bcrypt = Bcrypt(app)

class Customer:
    def validate_user(self, form_data):
        pass

    def create_user(self, form_data):
        mysql = connectToMySQL('bible_quest')

        query = 'INSERT INTO customers (name, email, address, phone_number, role_id, password, created_at, updated_at) VALUES (:name, :email, :address, :phone_number, :role_id, :password, NOW(), NOW());'
        data = {
            'name': form_data['name'],
            'email': form_data['email'],
            'address': form_data['address'],
            'role_id': form_data['role_id'],
            'phone_number': form_data['phone_number'],
            'password': bcrypt.generate_password_hash(form_data['password'])
        }
        mysql.query_db(query, data)
        
    def get_user_by_email(self, user_email):
        mysql = connectToMySQL('bible_quest')
        print('*'*100)
        query = 'SELECT role_id, email, password FROM customers WHERE email = :email;'
        data = {'email': user_email}
        return mysql.query_db(query, data)

    def verify_password(self, form_password, saved_password):
        if bcrypt.check_password_hash(saved_password, form_password):
            return True
        else:
            return False