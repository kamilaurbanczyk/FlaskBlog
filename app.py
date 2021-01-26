from flask import Flask, render_template

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/about')
def about():
    return render_template('about.html')


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


