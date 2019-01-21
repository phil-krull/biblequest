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

    def get_product(self, product_code, product_name):
        # print('in code get product')
        # print('*'*100)
        # set product to user
        # result = code.set_user_product(session['user_id'], product_code)
        check_product = code.get_user_product(session['user_id'], product_code)
        # print('^'*90)
        # print(check_product)
        if len(check_product) > 0:
            # print('yoyoyoyo')
            # product found
            # print(app.config['UPLOAD_FOLDER'])
            return send_from_directory(app.config['UPLOAD_FOLDER'], product_name+'.zip', as_attachment=True)
        else:
            # invalid code
            # print('in get_product invalid code condition')
            resp = jsonify({'message': 'You have no product with that code'})
            resp.status_code = 300
            # print(resp)
            return resp

    def get_user_products(self, user_id):
        pass

    def set_user_products(self, user_id, product_code):
        check_product = code.get_user_product(user_id, product_code)
        # print('+'*90)
        # print(len(check_product))
        if len(check_product) < 1:
            result = code.set_user_product(user_id, product_code)
            if result:
                return jsonify({'status': True, 'product': result})
            else:
                # invalid code
                resp = jsonify({'message': 'Please enter a valid product code'})
                resp.status_code = 300
                return resp
        else:
            resp = jsonify({'message': 'You are already associated with the product code'})
            resp.status_code = 300
            return resp