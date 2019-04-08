import os
from flask import Flask
app = Flask(__name__)

# email configuration
app.config.update(dict(
    DEBUG = True,
    MAIL_SERVER = 'smtp.gmail.com',
    MAIL_PORT = 587,
    MAIL_USE_TLS = True,
    MAIL_USE_SSL = False,
    MAIL_USERNAME = 'pkrull@codingdojo.com',
    MAIL_PASSWORD = '@NeverGiveUp24',
))
# set up directory for file upload
UPLOAD_FILES = os.path.abspath(os.path.dirname(__file__)) + '/config/uploaded_files/'
app.config['UPLOAD_FOLDER'] = UPLOAD_FILES
# set up session secret key
app.secret_key = 'My super secret key'
