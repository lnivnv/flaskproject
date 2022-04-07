from flask import Flask
from data import db_session
from data.tests import Tests
from data.questions import Questions

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'
title = ['Определи по картинке персонажа', 'Проверь свои знания во вселенной Гарри Поттера',
         'Определи какому персонажу пренадлежит эта цитата']
picture = ['Ханна Аббот.jpg', 'Невилл Долгопупс.jpg', 'Лили Поттер.jpg', 'Дин Томас.jpg', 'Астория Гринграсс.jpg']
title_question = ['1. Кто же эта очаровательная блондинка?', '2. А это у нас кто?',
                  '3. Кто же из слизеринок у нас здесь?', '4. Теперь пошли парни. Кто у нас здесь?', '5. А здесь?',
                  '1. Какой из этих вопросов Снегг не задавал Гарри Поттеру на самом первом уроке зельеварения?',
                  '2. А как зовут бабушку Невилла?',
                  '3. Кого из этих персонажей Слизнорт больше не приглашал в клуб слизней?',
                  '4. Какой из этих паролей не является паролем в башню Гриффиндора?',
                  '5. Как известно, Филч, хоть и родился сквибом, пытался научиться магии. Какой курс он проходил?',
                  '6. Какой из этих ингредиентов не входит в состав оборотного зелья?',
                  '7. А как звали родителей Волан-де-Морта?', '8. Полное имя Дамблдора?',
                  '9. У Дамблдора, как известно, есть шрам над левым коленом. Что он собой представляет?',
                  '10. Какую форму принимал патронус Полумны Лавгуд?',
                  '11. Кто из этих персонажей не был игроком в квиддич?',
                  '12. И напоследок, как зовут подругу Полной Дамы, которая рассказывает ей все сплетни замка?',
                  '1. Я не понимаю, почему в школу принимают не только таких, как мы, но и детей из других семей.',
                  '2. ...скажи мне, что не так... я могу тебе помочь...',
                  '3. Я говорю о твоей племяннице, Беллатриса. Она ведь только что вышла замуж за оборотня.',
                  '4. От нас требуют тренировать заклятие Круциатус на тех, кто оставлен после уроков за провинность…',
                  '5. Почему ты ещё жив?', '6. ... он был, пожалуй, самым храбрым человеком, которого я знал',
                  '7. Это же Гермиона. Если что непонятно, иди в библиотеку']


def test():
    db_session.global_init("db/tests.db")
    for i in range(len(title)):
        tests = Tests()
        tests.title = title[i]
        db_sess = db_session.create_session()
        db_sess.add(tests)
        db_sess.commit()
        # app.run()


def question():
    db_session.global_init("db/tests.db")
    for i in range(len(title_question)):
        questions = Questions()
        if i < 5:
            questions.test_id = 1
            questions.picture = picture[i]
        elif i < 17:
            questions.test_id = 2
        else:
            questions.test_id = 3
        questions.title = title_question[i]
        db_sess = db_session.create_session()
        db_sess.add(questions)
        db_sess.commit()


if __name__ == '__main__':
    test()
    question()
