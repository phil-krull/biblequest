from biblequest.config.mysqlconnection import connectToMySQL
from flask import render_template


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

    def registerCustomer(self):
        pass

    def login(self):
        pass

    def email(self):
        pass

    def users_page(self):
        pass

    