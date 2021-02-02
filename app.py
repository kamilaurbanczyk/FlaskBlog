from flask import Flask, render_template, flash, redirect, url_for, session, logging, request
from temporary_data import Articles
from passlib.hash import sha256_crypt
from forms import RegisterForm
from sqlalchemy import Integer, String, DateTime, ForeignKey, Text
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://malami:78z433XMn@localhost/myflaskblog'
db = SQLAlchemy(app)

# migrate = Migrate(app, db)
# manager = Manager(app)
# manager.add_command('db', MigrateCommand)

Articles = Articles()


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(Integer, primary_key=True)
    name = db.Column(String(50), unique=False)
    username = db.Column(String(30), unique=True)
    email = db.Column(String(100))
    password = db.Column(String(100))
    register_date = db.Column(DateTime)
    articles = db.relationship('Article', backref='user', lazy=True)


class Article(db.Model):
    __tablename__ = 'articles'
    id = db.Column(Integer, primary_key=True)
    title = db.Column(String(100))
    author = db.Column(String(30))
    user_id = db.Column(Integer, ForeignKey('users.id'), nullable=False)
    body = db.Column(Text)
    date = db.Column(DateTime)


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


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm(request.form)
    if request.method == 'POST' and form.validate():
        name = request.form['name']
        username = request.form['username']
        email = request.form['email']
        password = sha256_crypt.hash(str(request.form['password']))
        register_date = datetime.now()
        if User.query.filter_by(username=username).first():
            print("Username exists! Choose different username")
            return render_template('register.html', form=form)
        else:
            user = User(name=name, username=username, email=email, password=password, register_date=register_date)
            db.session.add(user)
            db.session.commit()
            return render_template('register.html', form=form)

    return render_template('register.html', form=form)


@app.route('/dashboard/<user_id>')
def dashboard(user_id):
    return render_template('dashboard.html', user_id)


@app.route('/article/<string:article_id>')
def display_article(article_id):
    # Later I will add MySQL database and find article by its id.
    article = {}
    return render_template('article.html', article=article)


@app.route('/add')
def add_post():
    return render_template('add_post.html')


@app.route('/edit')
def edit_post():
    return render_template('edit_post.html')


@app.teardown_appcontext
def shutdown_session(exception=None):
    pass


if __name__ == '__main__':
    app.run(debug=True)
