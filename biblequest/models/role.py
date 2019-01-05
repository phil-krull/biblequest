from biblequest.config.mysqlconnection import connectToMySQL

class Role:
    def get_roles(self):
        mysql = connectToMySQL('bible_quest')
        query = 'SELECT role_id, type FROM roles;'
        return mysql.query_db(query)

    def get_role(self, role='user'):
        mysql = connectToMySQL('bible_quest')
        query = 'SELECT role_id FROM roles WHERE type = %(role_type)s;'
        data = {'role_type': role}
        return mysql.query_db(query, data)[0]['role_id']
