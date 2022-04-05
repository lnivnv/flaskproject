from flask import Flask
from data import db_session
from data.tests import Tests

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'
title = ['Определи по картинке персонажа', 'Проверь свои знания во вселенной Гарри Поттера',
         'Определи какому персонажу пренадлежит эта цитата']


def main():
    db_session.global_init("db/tests.db")
    for i in range(len(title)):
        tests = Tests()
        tests.title = title[i]
        db_sess = db_session.create_session()
        db_sess.add(tests)
        db_sess.commit()
        # app.run()


if __name__ == '__main__':
    main()
