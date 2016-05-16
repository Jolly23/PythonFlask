# -*- coding: utf-8 -*-
import os
import sqlite3
from contextlib import closing
from flask import Flask, request, session, g, redirect, url_for, abort, render_template, flash
from config import *
from flask.ext.sqlalchemy import SQLAlchemy

# configuration
basedir = os.path.abspath(os.path.dirname(__file__))

DATABASE = os.path.join(basedir, 'flaskr.db')
DEBUG = True
SECRET_KEY = 'development key'
USERNAME = 'admin'
PASSWORD = 'admin'


app = Flask(__name__)
app.config.from_object(__name__)
# app.config.from_envvar('FLASKR_SETTINGS', silent=True)


if app.debug:
    import logging
    from logging.handlers import SMTPHandler
    from logging import Formatter
    mail_handler = SMTPHandler(mailhost=MAIL_HOST,
                               fromaddr=FROM_ADDR,
                               toaddrs=ADMINS,
                               subject=SUBJECT,
                               credentials=CREDENTIALS)
    mail_handler.setFormatter(Formatter('''
                        Message type:       %(levelname)s
                        Location:           %(pathname)s:%(lineno)d
                        Module:             %(module)s
                        Function:           %(funcName)s
                        Time:               %(asctime)s

                        Message:

                        %(message)s
                        '''))
    mail_handler.setLevel(logging.DEBUG)
    app.logger.addHandler(mail_handler)

    # import logging
    from logging.handlers import RotatingFileHandler

    file_handler = RotatingFileHandler('flaskr_logs', maxBytes=1024)
    file_handler.setFormatter(Formatter(
        '%(asctime)s %(levelname)s: %(message)s '
        '[in %(pathname)s:%(lineno)d]'
        ))
    file_handler.setLevel(logging.DEBUG)
    app.logger.addHandler(file_handler)


def connect_db():
    return sqlite3.connect(app.config['DATABASE'])


def init_db():
    with closing(connect_db()) as db:
        with app.open_resource('schema.sql', mode='r') as f:
            db.cursor().executescript(f.read())
        db.commit()


@app.before_request
def before_request():
    g.db = connect_db()


@app.teardown_request
def teardown_request(exception):
    db = getattr(g, 'db', None)
    if db is not None:
        db.close()
    g.db.close()


@app.route('/')
def show_entries():
    cur = g.db.execute('select title, text from entries order by id desc')
    entries = [dict(title=row[0], text=row[1]) for row in cur.fetchall()]
    return render_template('show_entries.html', entries=entries)


@app.route('/add', methods=['POST'])
def add_entry():
    if not session.get('logged_in'):
        abort(401)
    g.db.execute('insert into entries (title, text) values (?, ?)',
                 [request.form['title'], request.form['text']])
    g.db.commit()
    flash('New entry was successfully posted')
    return redirect(url_for('show_entries'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        if request.form['username'] != app.config['USERNAME']:
            error = 'Invalid username'
        elif request.form['password'] != app.config['PASSWORD']:
            error = 'Invalid password'
        else:
            session['logged_in'] = True
            flash('You were logged in')
            return redirect(url_for('show_entries'))
    return render_template('login.html', error=error)


@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    flash('You were logged out')
    return redirect(url_for('show_entries'))


if __name__ == '__main__':
    app.run()


