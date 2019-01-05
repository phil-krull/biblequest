import csv
# SystemRandom for cryptographically more secure version
from random import choice, SystemRandom
from string import ascii_lowercase, ascii_uppercase, digits
# use islice for adding newly created range of codes to DB
from itertools import islice
# import db connection
from biblequest.config.mysqlconnection import connectToMySQL

import os

LOCATION = os.path.abspath(os.path.dirname('biblequest')) + '/biblequest/config/book_codes/'

class Code():
    def __init__(self):
        self.files = ['bible_girls_party.csv','davids_mighty_men.csv', 'new_testament.csv', 'old_testament.csv']
        self.base_strings = ['BGP', 'DMM', 'BQNT', 'BQOT']

    def code_generator(self, number):
        for idx in range(len(self.base_strings)):
        # create 100000 codes for each file type
            with open(LOCATION + self.files[idx], 'a', newline='') as csvfile:
                spamwriter = csv.writer(csvfile, delimiter=' ', quotechar='|', quoting=csv.QUOTE_MINIMAL)
                for times in range(int(number)):
                    sub_string = ''.join(SystemRandom().choice(ascii_uppercase + digits + ascii_lowercase) for _ in range(14))
                    spamwriter.writerow([self.base_strings[idx] + sub_string])

    def code_saver(self):
        for idx in range(len(self.files)):
            # get last row saved in *_range db
            mysql = connectToMySQL('bible_quest')
            query = 'SELECT start, end FROM ' + self.files[idx][0:-4] + '_range;'
            # find the starting range, or create a new one
            try:
                result = mysql.query_db(query)[0]
                range_start = result['end']
                start = result['end'] + 1
                print(range_start)
            except IndexError:
                start = 1
                mysql = connectToMySQL('bible_quest')
                query = 'INSERT INTO ' + self.files[idx][0:-4] + '_range (start, created_at, updated_at) VALUES (%(start)s, Now(), Now());'
                data = {'start': start}
                mysql.query_db(query, data)
                range_start = 0
            with open(LOCATION + self.files[idx], newline='') as csvfile:
                # using range_start to only saved new codes generated on top of the existing codes
                spamreader = islice(csv.reader(csvfile, delimiter=' ', quotechar='|'), range_start, None)
                print('-'*20 + 'NEW FILE' + '-'*20)
                for row in spamreader:
                    mysql = connectToMySQL('bible_quest')
                    query = 'INSERT INTO ' + self.files[idx][0:-4] + ' (number, created_at, updated_at) VALUES (%(code)s, NOW(), NOW());'
                    data = {'code': row[0]}
                    end = mysql.query_db(query, data)
                try:
                    data = {'start': start, 'end': end}
                    query = 'UPDATE ' + self.files[idx][0:-4] + '_range SET start = %(start)s, end = %(end)s, updated_at = Now();'
                    mysql = connectToMySQL('bible_quest')
                    mysql.query_db(query, data)
                except:
                    pass

    def set_user_product(self, user_id, product_code):
        product_sub_str = product_code[:3]
        # indices = [i for i, elem in enumerate(mylist) if 'aa' in elem]
        product_idx_list = [idx for idx, elem in enumerate(self.base_strings) if product_sub_str in elem]
        try:
            product_idx = product_idx_list[0]
        except ValueError:
            print('invalid product substring')
            return False
        else:
            print(self.files[product_idx][0:-4])
            print(product_code)
            product_sub_table = self.files[product_idx][0:-4]
            mysql = connectToMySQL('bible_quest')
            # get product id from * table
            query = 'SELECT ' + product_sub_table + '_id FROM ' + product_sub_table + ' WHERE number = %(number)s;'
            data = {
                'number': product_code
            }
            product_id = mysql.query_db(query, data)
            print('^'*60)
            print(product_id)
            if len(product_id) > 0:
                #product found
                mysql = connectToMySQL('bible_quest')
                query = 'INSERT INTO ' + product_sub_table + '_has_customers (' + product_sub_table + '_' + product_sub_table  + '_id , customers_customer_id) VALUES (%(product)s, %(customer)s);'
                data = {
                    'product': product_id[0][product_sub_table+'_id'],
                    'customer': user_id
                }
                mysql.query_db(query, data)
                return True
            else:
                print('product not found')
                return False

    def get_user_products(self, user_id):
        products = []
        data = {
            'user_id': user_id
        }
        mysql = connectToMySQL('bible_quest')
        query = '''SELECT bible_girls_party.number FROM bible_girls_party
                    JOIN bible_girls_party_has_customers on bible_girls_party_has_customers.bible_girls_party_bible_girls_party_id = bible_girls_party.bible_girls_party_id
                    WHERE bible_girls_party_has_customers.customers_customer_id = %(user_id)s;'''
        product = mysql.query_db(query, data)
        try:
            product[0]['name'] = 'bible_girls_party'
            products.append(product[0])
        except:
            pass
        mysql = connectToMySQL('bible_quest')
        query = '''SELECT davids_mighty_men.number FROM davids_mighty_men
                    JOIN davids_mighty_men_has_customers on davids_mighty_men_has_customers.davids_mighty_men_davids_mighty_men_id = davids_mighty_men.davids_mighty_men_id
                    WHERE davids_mighty_men_has_customers.customers_customer_id = %(user_id)s;'''
        product = mysql.query_db(query, data)
        try:
            product[0]['name'] = 'davids_mighty_men'
            products.append(product[0])
        except:
            pass
        mysql = connectToMySQL('bible_quest')
        query = '''SELECT new_testament.number FROM new_testament
                    JOIN new_testament_has_customers on new_testament_has_customers.new_testament_new_testament_id = new_testament.new_testament_id
                    WHERE new_testament_has_customers.customers_customer_id = %(user_id)s;'''
        product = mysql.query_db(query, data)
        try:
            product[0]['name'] = 'new_testament'
            products.append(product[0])
        except:
            pass
        mysql = connectToMySQL('bible_quest')
        query = '''SELECT old_testament.number FROM old_testament
                    JOIN old_testament_has_customers on old_testament_has_customers.old_testament_old_testament_id = old_testament.old_testament_id
                    WHERE old_testament_has_customers.customers_customer_id = %(user_id)s;'''
        product = mysql.query_db(query, data)
        try:
            product[0]['name'] = 'old_testament'
            products.append(product[0])
        except:
            pass
        return products

    # get single product name and number, use for above method 