from flask import render_template, redirect, jsonify, session
from biblequest.models.customer import Customer
from biblequest.models.address import Address
from biblequest.models.role import Role
from biblequest.models.code import Code

customer = Customer()
address = Address()
role = Role()
code = Code()


class Customers():
    def index(self):
        return render_template('index.html')

    def register(self):
        pass

    def register_customer(self, form_data):
        # 1. validate new customer info
        user = customer.get_user_by_email(form_data['remail'])
        if user:
            resp = jsonify({'status': False, 'message': 'Email already in use!'})
            resp.status_code = 300
            return resp
        # response = customer.validate_user(form_data)
        # 2. validate customer address info
        # 3. get role id, defaults to user
        user_role = role.get_role()
        # 4. create and retrieve customer id(need role id, customer data)
        customer_id = customer.create_user(user_role, form_data)
        # print('-'*90)
        # print(customer_id)
        # 5. create customer address (need customer id, address data)
        address.set_customer_address(customer_id, form_data)

        # 6. set user_id in session
        session['user_id'] = customer_id
        # 7. set is_admin flag
        return jsonify({'status': True, 'message': True})

    def login_customer(self, form_data):
        user = customer.get_user_by_email(form_data['lemail'])
        # print(user)
        # print(form_data)
        # print('+'*90)
        if len(user) < 1:
            resp = jsonify({'status': False, 'message': 'Invalid email'})
            resp.status_code = 300
            return resp
            # return redirect('/')
        else:
            valid_login = customer.verify_password(user[0]['password'], form_data['lpassword'])
            if valid_login:
                session['user_id'] = user[0]['customer_id']
                if user[0]['roles_role_id'] == 1:
                    session['is_admin'] = True
                    return jsonify({'status': True, 'message': 'Is admin'})
                    # return redirect('/admin')
                else:
                    session['is_admin'] = False
                    # get all customer products
                    user_products = code.get_user_products(user[0]['customer_id'])
                    return jsonify({'status': True, 'message': 'Is user', 'products': user_products})
                    # return redirect('/users')
            else:
                return jsonify({'status': False, 'message': 'Invalid email/password combination'})
                # return redirect('/')

    def email(self):
        pass

    def users_page(self):
        if 'user_id' in session:
            user_products = code.get_user_products(session['user_id'])
            return jsonify({'status': True, 'message': 'Is user', 'products': user_products})
        else:
            return jsonify({'status': False})

    def logout(self):
        session.clear()
        return jsonify({'status': True, 'message': 'Successfully logged out'})

    