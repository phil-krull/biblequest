from biblequest import app
from flask_bcrypt import Bcrypt
# for file upload
from werkzeug.utils import secure_filename

from biblequest.controllers.customers import Customers # import the class
from biblequest.controllers.codes import Codes
customers = Customers()
codes = Codes()

from flask_mail import Mail, Message


import os
from flask import Flask, render_template, request, redirect, flash, session

print(os.path.abspath(os.path.dirname(__file__)))
print('+'*90)
UPLOAD_FILES = os.path.abspath(os.path.dirname(__file__)) + '/uploaded_files'
ALLOWED_EXTENSIONS = set(['zip'])

# app = Flask(__name__)

#set up mail server
app.config.update(dict(
    DEBUG = True,
    MAIL_SERVER = 'smtp.gmail.com',
    MAIL_PORT = 587,
    MAIL_USE_TLS = True,
    MAIL_USE_SSL = False,
    MAIL_USERNAME = 'pkrull@codingdojo.com',
    MAIL_PASSWORD = 'BowHunter24',
))

mail = Mail(app)

app.config['UPLOAD_FOLDER'] = UPLOAD_FILES
app.secret_key = 'My super secret key'

bcrypt = Bcrypt(app)

@app.route('/')
def index():
    return customers.index()

@app.route('/register')
def register():
    mysql = connectToMySQL('bible_quest')
    query = 'SELECT role_id, type FROM roles;'
    roles = mysql.query_db(query)

    return render_template('register.html', roles = roles)


@app.route('/registerCustomer', methods=['post'])
def register_customer():
    mysql = connectToMySQL('bible_quest')
    f = request.form
    print(request.form)
    query = 'INSERT INTO customers (name, email, address, phone_number, role_id, password, created_at, updated_at) VALUES (:name, :email, :address, :phone_number, :role_id, :password, NOW(), NOW());'
    data = {
        'name': f['name'],
        'email': f['email'],
        'address': f['address'],
        'role_id': f['role_id'],
        'phone_number': f['phone_number'],
        'password': bcrypt.generate_password_hash(f['password'])
    }
    mysql.query_db(query, data)

    return redirect('/')

@app.route('/loginCustomer', methods=['post'])
def login_customer():
    mysql = connectToMySQL('bible_quest')
    print('*'*100)
    query = 'SELECT role_id, email, password FROM customers WHERE email = :email;'
    data = {'email': request.form['email']}
    
    user = mysql.query_db(query, data)
    print(user)
    if user == []:
        return redirect('/')
    else:
        if bcrypt.check_password_hash(user[0]['password'], request.form['password']):
            if user[0]['role_id'] == 1:
                return redirect('/admin')
            else:
                return redirect('/users')
        else:
            return redirect('/')

@app.route('/email', methods=['POST'])
def email():
    name = request.form['name']
    email = request.form['email']
    message = request.form['message']

    msg = Message(subject=f'{ name } has sent you a new message', sender='biblequestcbc@gmail.com', body = message, reply_to=email, recipients=['philip.krull@hotmail.com'])
    # recipients=['biblequestcbc@gmail.com']
    mail.send(msg)

    return redirect('/')

# -------------------------------------------------------- admin routes --------------------------------------------------------
@app.route('/admin')
def admin_page():
    return render_template('admin.html')

@app.route('/admin/create_codes', methods=['POST'])
@app.route('/admin/create_codes/<amount>', methods=['POST'])
def create_codes(amount = 10000):
    return codes.generate_codes(amount)

@app.route('/admin/save_codes', methods=['POST'])
def save_codes():
    return codes.save_codes()

@app.route('/users')
def users_page():
    return render_template('user.html')

# upload a file
# will need to change the return statements
@app.route('/uploadFile', methods=['POST'])
def upload_file():
    print(request.files)
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            print('========================================= in file not in request =========================================')
            # return redirect('/admin')
        file = request.files['file']
        print(file.filename)
        print(file.filename.rsplit('.', 1)[1].lower())
        print(allowed_file(file.filename))
        print('-'*90)
        # if user does not select file, browser also
        # submit an empty part without filename
        if file.filename == '':
            flash('No selected file')
            print('========================================= in file name is empty =========================================')
            # return redirect('/admin')
        if file and allowed_file(file.filename):
            flash('Trying to add a file')
            print('========================================= in file saving file =========================================')
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            # file.save(os.path.join(app.config['UPLOAD_FOLDER']))
            # return redirect('/admin')
    return redirect('/admin')

# check for allowed file
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS