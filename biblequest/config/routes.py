from biblequest import app
from flask import Flask, render_template, request, redirect, flash, session
from biblequest.controllers.customers import Customers # import the class
from biblequest.controllers.codes import Codes
from biblequest.controllers.admins import Admins
from biblequest.config.cjwt import jwt_required, current_identity

customers = Customers()
codes = Codes()
admins = Admins()


# @app.route('/users')
# def users_page():
#     return render_template('user.html')

# register new customer
@app.route('/registerCustomer', methods=['post'])
def register_customer():
    return customers.register_customer(request.form)

# login customer handle in the /auth route
# @app.route('/loginCustomer', methods=['post'])
# def login_customer():
#     return customers.login_customer(request.form)

# logout customer
# @app.route('/logout', methods=['post'])
# @jwt_required()
# def logout_customer():
#     print('^'*90)
#     return customers.logout()

# display user page
@app.route('/customer_page')
@jwt_required()
def customer_checker():
    return customers.users_page()

# user edit route
# @app.route('/customer/<user_id>', methods=['put'])
# def edit(user_id):
#     return customers.edit_customer(user_id, request.form)

@app.route('/updateCustomer', methods=['post'])
@jwt_required()
def update():
    return customers.update_customer(request.form)


# -------------------------------------------------------- admin routes --------------------------------------------------------
# no admin routes will work
@app.route('/admin')
def admin_page():
    return redirect('/')
    # return render_template('admin.html')

@app.route('/admin/create_codes', methods=['POST'])
@app.route('/admin/create_codes/<amount>', methods=['POST'])
def create_codes(amount = 10000):
    return redirect('/')
    # return codes.generate_codes(amount)

@app.route('/admin/save_codes', methods=['POST'])
def save_codes():
    return redirect('/')
    # return codes.save_codes()

@app.route('/email', methods=['POST'])
def email():
    # name = request.form['name']
    # email = request.form['email']
    # message = request.form['message']

    # msg = Message(subject=f'{ name } has sent you a new message', sender='biblequestcbc@gmail.com', body = message, reply_to=email, recipients=['philip.krull@hotmail.com'])
    # # recipients=['biblequestcbc@gmail.com']
    # mail.send(msg)

    return admins.email_admin(request.form)

# -------------------------------------------------------- file upload routes --------------------------------------------------------
# upload a file
# will need to change the return statements
# no admin routes will work
@app.route('/uploadFile', methods=['POST'])
def upload_file():
    # print(request)
    # if request.method == 'POST':
    #     # check if the post request has the file part
    #     if 'file' not in request.files:
    #         flash('No file part')
    #         print('========================================= in file not in request =========================================')
    #         # return redirect('/admin')
    #     file = request.files['file']
    #     print(file.filename)
    #     print(file.filename.rsplit('.', 1)[1].lower())
    #     print(allowed_file(file.filename))
    #     print('-'*90)
    #     # if user does not select file, browser also
    #     # submit an empty part without filename
    #     if file.filename == '':
    #         flash('No selected file')
    #         print('========================================= in file name is empty =========================================')
    #         # return redirect('/admin')
    #     if file and allowed_file(file.filename):
    #         flash('Trying to add a file')
    #         print('========================================= in file saving file =========================================')
    #         filename = secure_filename(file.filename)
    #         file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
    #         # file.save(os.path.join(app.config['UPLOAD_FOLDER']))
    #         # return redirect('/admin')
    return redirect('/')
    # return admins.upload_file(request.files)

# -------------------------------------------------------- customer with code routes --------------------------------------------------------
@app.route('/enterCode/<code>', methods=['POST'])
@jwt_required()
def product_code(code):
    return codes.get_product(code, request.form['name'])

# need to authenticate this route
@app.route('/addProductToUser', methods=['POST'])
@jwt_required()
def addProductToUser():
    return codes.set_user_products(request.form['acode'])

# -------------------------------------------------------- root routes --------------------------------------------------------
# @app.route('/')
# def catch_all(path):
#     return render_template('index.html')

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def index(path):
    return customers.index()

def admin_checker():
    if session['is_admin']:
        return True
    else:
        return False