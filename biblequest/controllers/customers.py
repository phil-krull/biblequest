from biblequest.config.mysqlconnection import connectToMySQL
from flask import render_template, redirect
from biblequest.models.customer import Customer

customer = Customer()


class Customers():
    def index(self):
        mysql = connectToMySQL('bible_quest')
        print(mysql.query_db('SELECT * FROM customers'))
        # queries = []
        # queries.append('INSERT INTO roles (type, created_at, updated_at) VALUES ('admin', NOW(), NOW());')
        # queries.append('INSERT INTO roles (type, created_at, updated_at) VALUES ('user', NOW(), NOW());')
        # for query in queries:
        #     mysql.query_db(query)

        return render_template('index.html')

    def register(self):
        pass

    def register_customer(self, form_data):
        response = customer.validate_user(form_data)

        return redirect('/')

    def login_customer(self, form_data):
        user = customer.get_user_by_email(form_data['email'])
        if user == []:
            return redirect('/')
        else:
            valid_login = customer.verify_password(user[0]['password'], form_data['password'])
            if valid_login:
                if user[0]['role_id'] == 1:
                    return redirect('/admin')
                else:
                    return redirect('/users')
            else:
                return redirect('/')

    def email(self):
        pass

    def users_page(self):
        pass

    