from biblequest.models.admin import Admin
from flask import redirect, session, flash

admin = Admin()

class Admins:
    def upload_file(self, form_data):
        print(form_data)
        result = admin.upload_file(form_data)
        # will be returning message as json
        # flash(result[1])
        return redirect('/admin')

    def email_admin(self, form_data):
        # flash('email sent')
        admin.email_admin(form_data)
        return redirect('/')





# check for allowed file
# def allowed_file(filename):
#     return admin.file_is_valid(filename):
#     return '.' in filename and \
#            filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS