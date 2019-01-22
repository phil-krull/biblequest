import os
from biblequest import app
# for file upload
from werkzeug.utils import secure_filename
# import os
# print(os.path.abspath(os.path.dirname(__file__)))
# print('+'*90)
# UPLOAD_FILES = os.path.abspath(os.path.dirname(__file__)) + '/uploaded_files'
ALLOWED_EXTENSIONS = set(['zip'])

# for email
from flask_mail import Mail, Message
# app.config.update(dict(
#     DEBUG = True,
#     MAIL_SERVER = 'smtp.gmail.com',
#     MAIL_PORT = 587,
#     MAIL_USE_TLS = True,
#     MAIL_USE_SSL = False,
#     MAIL_USERNAME = 'pkrull@codingdojo.com',
#     MAIL_PASSWORD = 'BowHunter24',
# ))

mail = Mail(app)

class Admin:
    def upload_file(self, file):
        # print(file)
        # **************** add file name to db ****************
        # check if the post request has the file part
        if 'file' not in file:
            # print('========================================= in file not in request =========================================')
            return False, 'No file part'
        file = file['file']
        # print(file.filename)
        # print(file.filename.rsplit('.', 1)[1].lower())
        # print(self.file_is_valid(file.filename))
        # print('-'*90)
        # if user does not select file, browser also
        # submit an empty part without filename
        if file.filename == '':
            # print('========================================= in file name is empty =========================================')
            return False, 'No select file'
        if file and self.file_is_valid(file.filename):
            # print('========================================= in file saving file =========================================')
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            # file.save(os.path.join(app.config['UPLOAD_FOLDER']))
            # return redirect('/admin')
            return True, 'File uploaded'

    def email_admin(self, form_data):
        print("*"*90)
        print(form_data)
        name = form_data['name']
        email = form_data['email']
        message = form_data['message']
        print("*"*90)
        print(name)

        msg = Message(subject='%s has sent you a new message'%(name), sender='pkrull@codingdojo.com', body = message, reply_to=email, recipients=['biblequestcbc@gmail.com'])
        # recipients=['biblequestcbc@gmail.com']
        mail.send(msg)

    def file_is_valid(self, file_name):
        return '.' in file_name and file_name.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
    