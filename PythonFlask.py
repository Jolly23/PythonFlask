from flask import Flask, url_for, render_template

app = Flask(__name__)


@app.errorhandler(404)
def page_not_found(error):
    return render_template('page_not_found.html'), 404


@app.route('/')
def hello_world():
    return url_for('show_user_profile', username='Jolly')


@app.route('/hello')
def hello():
    return 'Hello World'


@app.route('/user/<username>')
def show_user_profile(username):
    # show the user profile for that user
    return 'User %s' % username


@app.route('/post/<int:post_id>')
def show_post(post_id):
    # show the post with the given id, the id is an integer
    return 'Post %d' % post_id


@app.route('/pro/')
def projects():
    return 'The project page'

if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port=5000)
