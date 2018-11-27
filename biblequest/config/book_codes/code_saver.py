import csv
from biblequest.config.mysqlconnection import connectToMySQL



# list of csv files
FILES = ['bible_girls_party.csv','davids_mighty_men.csv', 'new_testament.csv', 'old_testament.csv']

for idx in range(len(FILES)):
    with open(FILES[idx], newline='') as csvfile:
        spamreader = csv.reader(csvfile, delimiter=' ', quotechar='|')
        print('-'*20 + 'NEW FILE' + '-'*20)
        for row in spamreader:
            mysql = connectToMySQL('bible_quest')
            query = 'INSERT INTO codes number VALUES ("%(code)s");'
            data = {'code': row[0]}
            mysql.query_db(query, data)
            # print(row[0] + str(type(row[0])))