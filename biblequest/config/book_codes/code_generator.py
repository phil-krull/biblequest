# SystemRandom for cryptographically more secure version
from random import choice, SystemRandom
from string import ascii_lowercase, ascii_uppercase, digits

# list of base strings for codes
BASE_STRINGS = ['BGP', 'DMM', 'BQNT', 'BQOT']

# list of csv files
FILES = ['bible_girls_party.csv','davids_mighty_men.csv', 'new_testament.csv', 'old_testament.csv']


import csv

# loop through length of base string list and use index to match base string and file type for codes
for idx in range(len(BASE_STRINGS)):
# create 100000 codes for each file type
    with open(FILES[idx], 'w', newline='') as csvfile:
        spamwriter = csv.writer(csvfile, delimiter=' ', quotechar='|', quoting=csv.QUOTE_MINIMAL)
        for times in range(10):
            sub_string = ''.join(SystemRandom().choice(ascii_uppercase + digits + ascii_lowercase) for _ in range(14))
            spamwriter.writerow([BASE_STRINGS[idx] + sub_string])