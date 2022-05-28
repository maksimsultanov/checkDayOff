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
    if check_red_letter_days(datetime.date.today() + datetime.timedelta(days=3)):
        today_format = str(datetime.date.today() + datetime.timedelta(days=3))
        todayis = today_format[8:10] + "-" + today_format[5:7] + "-" + today_format[0:4]
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
