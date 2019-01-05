from biblequest.config.mysqlconnection import connectToMySQL
from flask import jsonify, session

from biblequest import app
from flask_bcrypt import Bcrypt

bcrypt = Bcrypt(app)

class Customer:
    def validate_user(self, form_data):
        print('%'*90)
        print(form_data)
        # 1. validate purpose
        return jsonify({'success': True})

    # validate purpose, return true if purpose id matches purpose name in db
    def validate_purpose(self, purpose_id, purpose_name):
        mysql = connectToMySQL('bible_quest')
        query = 'SELECT * FROM purpose WHERE purpose_id = %(purpose_id)s AND purpose=%(purpose_name)s;'
        data = {
            'purpose_id': purpose_id,
            'purpose_name': purpose_name
        }
        result = mysql.query_db(query, data)
        return (True, False)[len(result) == 0]

    # create user and return id
    def create_user(self, role_id, form_data):
        mysql = connectToMySQL('bible_quest')
        query = 'INSERT INTO customers (name, email, phone_number, roles_role_id, purpose_purpose_id, password, created_at, updated_at) VALUES (%(name)s, %(email)s, %(phone_number)s, %(role_id)s, %(purpose_id)s, %(password)s, NOW(), NOW());'
        data = {
            'name': form_data['rname'],
            'email': form_data['remail'],
            'role_id': role_id,
            'purpose_id': int(form_data['rpurpose']),
            'phone_number': form_data['rphone_number'].replace("-", ""),
            'password': bcrypt.generate_password_hash(form_data['rpassword']).decode('utf-8')
        }
        return mysql.query_db(query, data)
        
    def get_user_by_email(self, user_email):
        mysql = connectToMySQL('bible_quest')
        print('*'*100)
        query = 'SELECT customer_id, roles_role_id, email, password FROM customers WHERE email = %(email)s;'
        data = {'email': user_email}
        return mysql.query_db(query, data)

    def verify_password(self, saved_password, form_password):
        print('saved_password')
        print(saved_password)
        print('form_password')
        print(form_password)
        if bcrypt.check_password_hash(saved_password, form_password):
            return True
        else:
            return False
