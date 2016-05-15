# -*- coding: utf-8 -*-
from flask import Flask, url_for, render_template, request, redirect

app = Flask(__name__)


@app.errorhandler(404)
def page_not_found(error):
    return render_template('page_not_found.html'), 404


@app.route('/')
def hello_world():
    return redirect(url_for('show_user_profile', username='Jolly'))


@app.route('/hello/')
@app.route('/hello/<name>')
def hello(name=None):
    return render_template('hello.html', name=name)


@app.route('/user/<username>')
def show_user_profile(username):
    # show the user profile for that user
    return 'User %s' % username


@app.route('/pro/')
def projects():
    return 'The project page'


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        return u'登录成功!'
    else:
        return u'准备登陆!'


if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port=5000)
