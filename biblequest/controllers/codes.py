from biblequest.models.code import Code
from flask import redirect, send_from_directory, session, jsonify
from biblequest import app

code = Code()

class Codes():
    def generate_codes(self, amount):
        code.code_generator(amount)
        return redirect('/')

    def save_codes(self):
        code.code_saver()
        return redirect('/')

    def get_product(self, product_code):
        print('in code get product')
        print('*'*100)
        # set product to user
        result = code.set_user_product(session['user_id'], product_code)
        if result:
            # product found
            print(app.config['UPLOAD_FOLDER'])
            return send_from_directory(app.config['UPLOAD_FOLDER'], 'testfile.txt.zip', as_attachment=True)
        else:
            # invalid code
            print('in get_product invalid code condition')
            resp = jsonify({'message': 'Please enter a valid product code'})
            resp.status_code = 300
            print(resp)
            return resp

    def get_user_products(self, user_id):
        pass

    def set_user_products(self, user_id, product_code):
        pass