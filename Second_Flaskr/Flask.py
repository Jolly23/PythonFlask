# -*- coding: utf-8 -*-
import os
import sqlite3
from flask import Flask, request, session, g, redirect, url_for, abort, render_template, flash
from flask.ext.sqlalchemy import SQLAlchemy

# configuration
basedir = os.path.abspath(os.path.dirname(__file__))

DATABASE = 'sqlite:///' + os.path.join(basedir, 'app.db')
DEBUG = True
SECRET_KEY = 'development key'
USERNAME = 'admin'
PASSWORD = 'admin'


app = Flask(__name__)
app.config.from_object(__name__)
'''
app = Flask(__name__)
app.config.from_object('config')
db = SQLAlchemy(app)
'''