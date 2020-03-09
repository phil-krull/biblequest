from biblequest.config.mysqlconnection import connectToMySQL
from flask import jsonify, session
import re
from biblequest import app
from flask_bcrypt import Bcrypt
from biblequest.config.cjwt import JWT

bcrypt = Bcrypt(app)

def authenticate(email, password):
    try:
        user = customer.get_user_by_email(email)[0]

        if user and customer.verify_password(user['password'], password):
            return user
    except:
        pass

def identity(payload):
    return customer.get_user_by_id(payload['identity'])

jwt = JWT(app, authenticate, identity)

# from biblequest import app, bcrypt

class Customer:
    def validate_user(self, user_info):
        # print('%'*90)
        # print(form_data)
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
            'password': self.hash_password(form_data['rpassword'])
        }
        return mysql.query_db(query, data)
        
    def get_user_by_email(self, user_email):
        mysql = connectToMySQL('bible_quest')
        # print('*'*100)
        query = 'SELECT customer_id, roles_role_id, email, password FROM customers WHERE email = %(email)s;'
        data = {'email': user_email}
        return mysql.query_db(query, data)

    def get_user_by_id(self, user_id):
        mysql = connectToMySQL('bible_quest')
        query = 'SELECT * FROM customers WHERE customer_id = %(user_id)s';
        data = {
            'user_id': user_id
        }
        return mysql.query_db(query, data)[0]

    def validate_password(self, password):
        return re.match('^(?=.*[a-z])(?=.*[A-Z])(?=.*[0-9])(?=.*[!@#\$%\^&\*])(?=.{8,})', password)

    def verify_password(self, saved_password, form_password):
        if bcrypt.check_password_hash(saved_password, form_password):
            return True
        else:
            return False

    def hash_password(self, user_password):
        return bcrypt.generate_password_hash(user_password).decode('utf-8')

    # find and update user
    def update_user_password(self, user_id, post_data):
        print('*'*90)
        print(post_data)
        print(user_id)
        # validate user data
        if post_data['new_password'] != post_data['new_confirm_password'] or not self.validate_password(post_data['new_password']):
            return False

        mysql = connectToMySQL('bible_quest')
        query = 'SELECT password FROM customers WHERE customer_id = %(customer_id)s;'
        data = {'customer_id': user_id}
        user = mysql.query_db(query, data)
        if len(user) > 0:
            # verify password
            if self.verify_password(user[0]['password'], post_data['old_password']):
                # change password
                query = 'UPDATE customer SET password = %(password)s WHERE customer_id=%(customer_id)s;'
                data={
                    'customer_id':user_id,
                    'password': self.hash_password(post_data['new_password'])
                }
                mysql = connectToMySQL('bible_quest')
                mysql.query_db(query, data)
                return True
            else:
                return False
        else:
            return False
        # find user by id, and verify current password
        # hash new password and save the update

customer = Customer()