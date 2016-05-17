# -*- coding: utf-8 -*-
import os

# configuration
basedir = os.path.abspath(os.path.dirname(__file__))
DATABASE = os.path.join(basedir, 'flaskr.db')
DEBUG = True
SECRET_KEY = 'development key'
USERNAME = 'admin'
PASSWORD = 'admin'

MAIL_HOST = 'applesmtp.163.com'
FROM_ADDR = 'server-error@example.com'
ADMINS = ['pilot_lei@foxmail.com']  # To address
SUBJECT = 'YourApplication Failed'
CREDENTIALS = ('lionel_lei@163.com', '*')
