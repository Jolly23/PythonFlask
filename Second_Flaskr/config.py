# -*- coding: utf-8 -*-
import os

# configuration
basedir = os.path.abspath(os.path.dirname(__file__))
DATABASE = os.path.join(basedir, 'flaskr.db')
SERVER_PORT = 18909
DEBUG = True
SECRET_KEY = 'development key'
USERNAME = 'admin'
PASSWORD = 'admin'

MAIL_HOST = 'applesmtp.163.com'
FROM_ADDR = 'server-error@example.com'
ADMINS = ['pilot_lei@foxmail.com']  # To address
SUBJECT = 'YourApplication Failed'
CREDENTIALS = ('lionel_lei@163.com', '*')

UPLOAD_FOLDER = '/root/PythonFlask/Second_Flaskr/tmp'
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])
