from biblequest import app
# from flask_bcrypt import Bcrypt
# for file upload
# from werkzeug.utils import secure_filename

from biblequest.controllers.customers import Customers # import the class
from biblequest.controllers.codes import Codes
from biblequest.controllers.admins import Admins

customers = Customers()
codes = Codes()
admins = Admins()

# from flask_mail import Mail, Message


# import os
from flask import Flask, render_template, request, redirect, flash, session

# print(os.path.abspath(os.path.dirname(__file__)))
# print('+'*90)
# UPLOAD_FILES = os.path.abspath(os.path.dirname(__file__)) + '/uploaded_files'
# ALLOWED_EXTENSIONS = set(['zip'])

# app = Flask(__name__)

#set up mail server
# app.config.update(dict(
#     DEBUG = True,
#     MAIL_SERVER = 'smtp.gmail.com',
#     MAIL_PORT = 587,
#     MAIL_USE_TLS = True,
#     MAIL_USE_SSL = False,
#     MAIL_USERNAME = 'pkrull@codingdojo.com',
#     MAIL_PASSWORD = 'BowHunter24',
# ))

# mail = Mail(app)

# app.config['UPLOAD_FOLDER'] = UPLOAD_FILES
# app.secret_key = 'My super secret key'

# bcrypt = Bcrypt(app)



# -------------------------------------------------------- customer routes --------------------------------------------------------
# do not need when using front end frame work
# @app.route('/register')
# def register():
#     mysql = connectToMySQL('bible_quest')
#     query = 'SELECT role_id, type FROM roles;'
#     roles = mysql.query_db(query)

#     return render_template('register.html', roles = roles)
@app.route('/users')
def users_page():
    return render_template('user.html')


@app.route('/registerCustomer', methods=['post'])
def register_customer():
    return customers.register_customer(request.form)

@app.route('/loginCustomer', methods=['post'])
def login_customer():
    return customers.login_customer(request.form)

@app.route('/logout', methods=['post'])
def logout_customer():
    return customers.logout()

@app.route('/customer')
def customer_checker():
    return customers.users_page()


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
def product_code(code):
    return codes.get_product(code, request.form['name'])

# need to authenticate this route
@app.route('/addProductToUser', methods=['POST'])
def addProductToUser():
    return codes.set_user_products(session['user_id'], request.form['acode'])

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