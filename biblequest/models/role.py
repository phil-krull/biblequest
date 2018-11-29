from biblequest.config.mysqlconnection import connectToMySQL

class Role:
    def get_roles(self):
        mysql = connectToMySQL('bible_quest')
        query = 'SELECT role_id, type FROM roles;'
        return mysql.query_db(query)
