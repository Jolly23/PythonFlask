# -*- coding: utf-8 -*-

import sqlite3
from contextlib import closing
from flask import Flask, request, session, g, redirect, url_for, abort, render_template, flash
import os
from werkzeug import secure_filename
from flask import send_from_directory

app = Flask(__name__)
app.config.from_object('config')

ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])


if not app.debug:
    import logging
    from logging.handlers import SMTPHandler
    from logging import Formatter
    mail_handler = SMTPHandler(mailhost=app.config['MAIL_HOST'],
                               fromaddr=app.config['FROM_ADDR'],
                               toaddrs=app.config['ADMINS'],
                               subject=app.config['SUBJECT'],
                               credentials=app.config['CREDENTIALS'])
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


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in  ALLOWED_EXTENSIONS


@app.route('/up', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        file = request.files['file']
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            # file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            file.save(os.path.join('/root/PythonFlask/Second_Flaskr/tmp', filename))
            return redirect(url_for('uploaded_file',
                                    filename=filename))
    return '''
    <!doctype html>
    <title>Upload new File</title>
    <h1>Upload new File</h1>
    <form action="" method=post enctype=multipart/form-data>
      <p><input type=file name=file>
         <input type=submit value=Upload>
    </form>
    '''


@app.route('/up/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)


if __name__ == '__main__':
    app.run(port=app.config['SERVER_PORT'])


