from flask import Flask, render_template, flash, redirect, url_for, session, logging, request
from temporary_data import Articles
from passlib.hash import sha256_crypt
from forms import RegisterForm, LoginForm, ArticleForm
from sqlalchemy import Integer, String, DateTime, ForeignKey, Text
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from functools import wraps

from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://malami:78z433XMn@localhost/myflaskblog'
app.secret_key = '_5#y2L"F4Q8z\n\xec]/'
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


def is_logged_in(my_func):
    @wraps(my_func)
    def wrapper(*args, **kwargs):
        if 'username' in session:
            return my_func(*args, **kwargs)
        else:
            flash('Not authenticated! Please log in.')
            return redirect(url_for('login'))
    return wrapper


@app.route('/')
def index():
    articles = Article.query.order_by(Article.id.desc()).limit(3)
    return render_template('index.html', articles=articles)


@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/contact')
def contact():
    return render_template('contact.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm(request.form)
    if request.method == 'POST' and form.validate():
        username = request.form['username']
        password = request.form['password']

        this_user = User.query.filter_by(username=username).first()

        if this_user:
            if sha256_crypt.verify(password, this_user.password):
                session['logged in'] = True
                session['username'] = this_user.username
                session.permanent = False
                flash("You are now logged in")
                return redirect(url_for('index'))
            else:
                flash('Wrong password! Try again')
                return render_template('login.html', form=form)
        else:
            flash('This user not exists. Try again.')
            return render_template('login.html', form=form)

    return render_template('login.html', form=form)


@app.route('/logout')
@is_logged_in
def logout():
    session.clear()
    flash('You are now logged out.')
    return redirect(url_for('login'))


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
            flash('Username exists! Choose different username')
            return render_template('register.html', form=form)
        else:
            flash('You were successfully registered')
            user = User(name=name, username=username, email=email, password=password, register_date=register_date)
            db.session.add(user)
            db.session.commit()
            return render_template('index.html')

    return render_template('register.html', form=form)


@app.route('/dashboard')
@is_logged_in
def dashboard():
    user = User.query.filter(User.username == session['username']).first()
    num_articles = len(user.articles)
    articles = Article.query.filter(Article.author == session['username']).all()
    return render_template('dashboard.html', user=user, num_articles=num_articles, articles=articles)


@app.route('/article/<string:article_id>')
def display_article(article_id):
    article = Article.query.filter(Article.id == article_id).first()
    return render_template('article.html', article=article)


@app.route('/add', methods=['POST', 'GET'])
@is_logged_in
def add_article():
    form = ArticleForm(request.form)
    if request.method == 'POST' and form.validate():
        title = request.form['title']
        body = request.form['body']
        author = session['username']
        user_id = User.query.filter_by(username=author).first().id
        date = datetime.now()

        article = Article(title=title, body=body, author=author, user_id=user_id, date=date)
        db.session.add(article)
        db.session.commit()

        flash("Article added successfully!")
        return render_template('index.html')

    return render_template('add_article.html', form=form)


@app.route('/edit')
def edit_post():
    return render_template('edit_post.html')


@app.teardown_appcontext
def shutdown_session(exception=None):
    pass


if __name__ == '__main__':
    app.run(debug=True)
