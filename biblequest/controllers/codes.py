from biblequest.models.code import Code
from flask import redirect

code = Code()

class Codes():
    def generate_codes(self, amount):
        code.code_generator(amount)
        return redirect('/')

    def save_codes(self):
        code.code_saver()
        return redirect('/')