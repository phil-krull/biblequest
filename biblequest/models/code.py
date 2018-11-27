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