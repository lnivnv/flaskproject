from flask import Flask, render_template, flash, redirect, url_for, session, request
from main_Masha import tests_tests, tests_questions, tests_answers
import sqlite3
from wtforms import Form, StringField, PasswordField, validators
from passlib.hash import sha256_crypt
from functools import wraps

app = Flask(__name__)

Tests = tests_tests()
Question = tests_questions()
Answer = tests_answers()
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = '123456'
app.config['MYSQL_DB'] = 'myflaskapp'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'


@app.route('/')
@app.route('/home')
def index():
    return render_template('home.html')


@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/tests')
def tests():
    return render_template('tests.html', tests=Tests)


@app.route('/test/<title>')
def test(title):
    return render_template('test.html', title=title, tests=Tests, Question=Question, answer=Answer)


class RegisterForm(Form):
    name = StringField('Name', [validators.Length(min=1, max=50)])
    username = StringField('Username', [validators.Length(min=4, max=25)])
    email = StringField('Email', [validators.Length(min=6, max=50)])
    password = PasswordField('Password', [
        validators.DataRequired(),
        validators.EqualTo('confirm', message='Passwords do not match')
    ])
    confirm = PasswordField('Confirm Password')


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm(request.form)
    if request.method == 'POST' and form.validate():
        name = form.name.data
        email = form.email.data
        username = form.username.data
        password = sha256_crypt.encrypt(str(form.password.data))
        con = sqlite3.connect("users.db")
        cur = con.cursor()
        try:
            cur.execute("""INSERT INTO users(name, email, username, password) VALUES(?, ?, ?, ?)""",
                        (name, email, username, password,))
            con.commit()
            con.close()
            return redirect(url_for('login'))
        except Exception as e:
            error = 'имя пользователя может быть занято'
            return render_template('register.html', form=form, error=error)

    return render_template('register.html', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password_candidate = request.form['password']
        con = sqlite3.connect("users.db")
        cur = con.cursor()
        result = cur.execute("""SELECT * FROM users WHERE username = ?""", [username, ])
        if result:
            data = cur.fetchone()
            password = data[4]
            if sha256_crypt.verify(password_candidate, password):
                session['logged_in'] = True
                session['username'] = username
                flash('You are now logged in', 'success')
                return redirect('/home')
            else:
                error = 'Invalid login or password'
                return render_template('login.html', error=error)
        else:
            error = 'Username not found'
            return render_template('login.html', error=error)
    return render_template('login.html')


def is_logged_in(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return f(*args, **kwargs)
        else:
            flash('Unauthorized, Please login', 'danger')
            return redirect(url_for('home'))

    return wrap


@app.route('/logout')
@is_logged_in
def logout():
    session.clear()
    flash('You are now logged out', 'success')
    return redirect('/home')


if __name__ == '__main__':
    app.secret_key = 'secret123'
    app.run(port=8000, host='127.0.0.1')
