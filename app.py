from flask import Flask, render_template
from temporary_data import Articles

app = Flask(__name__)

Articles = Articles()

@app.route('/')
def index():
    return render_template('index.html', articles=Articles)


@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/contact')
def contact():
    return render_template('contact.html')


@app.route('/login')
def login():
    return render_template('login.html')


@app.route('/register')
def register():
    return render_template('register.html')


@app.route('/dashboard/<user_id>')
def dashboard(user_id):
    return render_template('dashboard.html', user_id)


@app.route('/add')
def add_post():
    return render_template('add_post.html')


@app.route('/edit')
def edit_post():
    return render_template('edit_post.html')


if __name__ == '__main__':
    app.run(debug=True)


