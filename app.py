from flask import Flask, render_template, flash, redirect, url_for, session, request
from passlib.hash import sha256_crypt
from forms import RegisterForm, LoginForm, ArticleForm
from sqlalchemy import Integer, String, DateTime, ForeignKey, Text
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from functools import wraps
from secrets import SECRET_KEY, DATABASE_URI
import re


app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URI
app.secret_key = SECRET_KEY
db = SQLAlchemy(app)


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


def first_paragraph(text):
    pattern = re.compile(r'<p>.*?</p>')
    match_object = pattern.search(text)
    return match_object.group()


@app.route('/')
def index():
    articles = Article.query.order_by(Article.id.desc()).limit(3)

    # Return only first paragraph of every article to be displayed.
    for article in articles:
        article.body = first_paragraph(article.body)

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


@app.route('/all_articles')
def display_articles_list():
    articles = Article.query.order_by(Article.title).all()
    return render_template('all_articles.html', articles=articles)


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


@app.route('/edit/<string:article_id>', methods=['GET', 'POST'])
@is_logged_in
def edit_article(article_id):
    article = Article.query.filter(Article.id == article_id).first()

    if article.author == session['username']:

        form = ArticleForm()
        form.title.data = article.title
        form.body.data = article.body

        if request.method == 'POST' and form.validate():
            title = request.form['title']
            body = request.form['body']

            article.title = title
            article.body = body
            db.session.commit()

            flash('Article was successfully updated')
            return redirect(url_for('index'))
    else:
        flash('No permission to perform action')
        return redirect(url_for('index'))

    return render_template('edit_article.html', form=form)


@app.route('/delete/<string:article_id>')
@is_logged_in
def delete_article(article_id):
    article = Article.query.filter(Article.id == article_id).first()

    if article.author == session['username']:
        db.session.delete(article)
        db.session.commit()

        flash('Article was successfully deleted')
        return redirect(url_for('index'))

    else:
        flash('No permission to perform action')
        return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(debug=True)
