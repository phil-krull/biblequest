from biblequest.config.mysqlconnection import connectToMySQL

class Address:
    def validate_address(self, form_data):
        pass

    def get_address_type(self, address_type='shipping'):
        mysql = connectToMySQL('bible_quest')
        query = 'SELECT (address_type_id) from address_type WHERE address_type_description=%(address_type)s;'
        data = {'address_type': address_type}
        return mysql.query_db(query, data)[0]

    def get_address(self, customer_id):
        mysql = connectToMySQL('bible_quest')
        query = 'SELECT * FROM customers_addresses JOIN address_type ON address_type.address_type_id = customers_addresses.address_type_id JOIN address ON address.address_id = customers_addresses.address_id WHERE customers_addresses.customer_id = %(customer_id)s;'
        data = {'customer_id': customer_id}
        return mysql.query_db(query, data)

    # create address and returns id
    def set_address(self, form_data):
        mysql = connectToMySQL('bible_quest')
        query = 'INSERT INTO address (line_1, city, state, zip, created_at, updated_at) VALUES (%(address)s, %(city)s, %(state)s, %(zip)s, NOW(), NOW());'
        data = {
            'address': form_data['raddress'],
            'city': form_data['rcity'],
            'state': form_data['rstate'],
            'zip': form_data['rzip']
        }
        return mysql.query_db(query, data)

    # create new customer
    def set_customer_address(self, customer_id, form_data):
        address_id = self.set_address(form_data)
        # get address type id, defaults to shipping
        address_type_id = self.get_address_type()
        mysql = connectToMySQL('bible_quest')
        query = 'INSERT INTO customers_addresses (customer_id, address_id, address_type_id) VALUES (%(customer_id)s, %(address_id)s, %(address_type_id)s);'
        data = {
            'customer_id': customer_id,
            'address_id': address_id,
            'address_type_id': address_type_id['address_type_id']
        }
        mysql.query_db(query, data)
