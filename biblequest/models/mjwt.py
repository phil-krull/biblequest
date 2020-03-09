from biblequest.config.mysqlconnection import connectToMySQL
from datetime import timedelta
# from biblequest import bcrypt
from biblequest.models.customer import Customer

customer = Customer()


# def authenticate(email, password):
#     mysql = connectToMySQL('bible_quest')
#     query = 'SELECT * FROM customers WHERE email = %(form_email)s';
#     data = {
#         'form_email': email
#     }
#     user = mysql.query_db(query, data)[0]

#     if user and bcrypt.check_password_hash(user['password'], password):
#         return user

# def identity(payload):
#     mysql = connectToMySQL('bible_quest')
#     query = 'SELECT * FROM customers WHERE customer_id = %(user_id)s';
#     data = {
#         'user_id': payload['identity']
#     }

#     return mysql.query_db(query, data)[0]

def authenticate(email, password):
    mysql = connectToMySQL('bible_quest')
    query = 'SELECT * FROM customers WHERE email = %(form_email)s';
    data = {
        'form_email': email
    }
    user = customer.get_user_byEmail(email)[0]

    if user and bcrypt.check_password_hash(user['password'], password):
        return user

def identity(payload):
    # mysql = connectToMySQL('bible_quest')
    # query = 'SELECT * FROM customers WHERE customer_id = %(user_id)s';
    # data = {
    #     'user_id': payload['identity']
    # }

    return customer.get_user_by_id(payload['identity'])