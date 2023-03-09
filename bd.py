import sqlite3

def connect():
    try:
        sqlite_connection = sqlite3.connect('/home/artem/PycharmProjects/utv/db.sqlite3')
        cursor = sqlite_connection.cursor()
        print("База данных создана и успешно подключена к SQLite")
    except:
        print("Не удалось подключиться к БД")
