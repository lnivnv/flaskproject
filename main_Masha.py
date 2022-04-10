from flask import Flask
from data import db_session
from data.tests import Tests
from data.questions import Questions
import csv

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'


def test():
    db_session.global_init("db/tests.db")
    with open('tests.csv', encoding="utf8") as csvfile:
        reader = csv.reader(csvfile, delimiter=';', quotechar='"')
        for index, row in enumerate(reader):
            tests = Tests()
            tests.title = row[0]
            db_sess = db_session.create_session()
            db_sess.add(tests)
            db_sess.commit()
        # app.run()


def question():
    db_session.global_init("db/tests.db")
    with open('questions.csv', encoding="utf8") as csvfile:
        reader = csv.reader(csvfile, delimiter=';', quotechar='"')
        for index, row in enumerate(reader):
            questions = Questions()
            if index < 5:
                questions.test_id = 1
                questions.picture = row[1]
            elif index < 17:
                questions.test_id = 2
            else:
                questions.test_id = 3
            questions.title = row[0]
            db_sess = db_session.create_session()
            db_sess.add(questions)
            db_sess.commit()


if __name__ == '__main__':
    test()
    question()
