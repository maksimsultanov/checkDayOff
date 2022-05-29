"""
Этот скрипт проверяет, наступит ли прааздничный день через 3 дня, если да то происходит
уведомление пользователей Битрикс
"""
import datetime  # Импорт модуля для работы с датой/временем
import requests  # Библиотека для работы с WEB запросами
import bitrix24  # Бибилиотека для работы с API Битрикс24

# набор данных для проверки текущей даты, актуален для 2022 года
RED_LETTER_DAYS = dict([("2022-01-01", "Новогодние каникулы"), ("2022-01-02", "Новогодние каникулы"),
                        ("2022-01-03", "Новогодние каникулы"), ("2022-01-04", "Новогодние каникулы"),
                        ("2022-01-05", "Новогодние каникулы"), ("2022-01-06", "Новогодние каникулы"),
                        ("2022-01-07", "Рождество Христово"), ("2022-02-23", "День защитника Отечества"),
                        ("2022-03-08", "Международный женский день"), ("2022-05-01", "Праздник весны и труда"),
                        ("2022-05-09", "День Победы"), ("2022-06-12", "День России"),
                        ("2022-11-04", "День народного единства")])

# Подключение к rest api через webhook
bx24 = bitrix24.Bitrix24('https://b24-lvyl0a.bitrix24.ru/rest/1/f2tq0ulf4ewiovwy/')


def check_red_letter_days(check_date):
    """
    :param check_date: доата для проверки, наступит ли через 3 дня праздник
    :return: результат проверки текущей даты
    """
    return str(check_date) in RED_LETTER_DAYS


def create_red_letter_day_task():
    """
    Функция выполняет добавление задачи в Битрикс за 3 дня до праздника
    Полея для добавления задачи описаны тут https://dev.1c-bitrix.ru/rest_help/tasks/task/tasks/tasks_task_getFields.php
    Метод добавления задачи https://dev.1c-bitrix.ru/rest_help/tasks/task/tasks/tasks_task_add.php
    Подключение к rest api Битрикс24 происходит через webhook https://dev.1c-bitrix.ru/learning/course/index.php?COURSE_ID=99&LESSON_ID=8581
    Использовались следующие поля:
    TITLE 	Название 	string
    RESPONSIBLE_ID 	Исполнитель 	integer
    :return:
    """

    # определение даты которую нужно проверить
    check_date = datetime.date.today() + datetime.timedelta(days=3)
    # Проверка, будет ли через 3 дня праздник
    if check_red_letter_days(check_date):
        # Дата прошедная проверку, преобразуется в строку
        today_format = str(check_date)
        # Далее полученная строка приводится к виду принятому в РФ для написания даты
        todayis = today_format[8:10] + "-" + today_format[5:7] + "-" + today_format[0:4]
        # Попытка создать задачу в Битрикс24
        # В случае неуспеха выводится сообщение об ошибке от Битрикс24
        try:
            bx24.callMethod('tasks.task.add',
                            fields={'TITLE': todayis + ' ' + RED_LETTER_DAYS[today_format], 'RESPONSIBLE_ID': 1})
        except bitrix24.BitrixError as message:
            print(message)
            pass
        print("Проверка выполнена")
    else:
        print("В ближайшее время праздников не предвидится")


if __name__ == '__main__':
    """
    Запуск скрипта просисходит только если файл main.py выполняется
    """
    create_red_letter_day_task()
