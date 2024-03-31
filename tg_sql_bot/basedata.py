import sqlite3
from aiogram import types


def connet():
    global connection
    global cursor
    connection = sqlite3.connect('calendar_data.db')
    cursor = connection.cursor()
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Users (
    id INTEGER,
    calendar TEXT
    )
    ''')


def add_bd(message: types.Message):
    cursor.execute('INSERT INTO Users (id, calendar) VALUES (?, ?)', (message.from_user.id, message.text))
    message.answer('Записал!')
    connection.commit()


def show_all_bd(message: types.Message):
    cursor.execute('SELECT calendar FROM Users where id = ?', (message.from_user.id, ))
    results = cursor.fetchall()
    k = 1
    vse_nap = {}
    for nap in results:
        nap = nap[0].split(':')
        vse_nap[k] = f'{nap[0]} {nap[1]} {nap[2]}'
        k += 1
    return vse_nap


def delete_bd(message: types.Message):
    base_info = show_all_bd(message)
    number = message.text
    try:
        curr_result = base_info[int(number)].replace(' ', ':', 2)
        cursor.execute('DELETE FROM Users WHERE calendar = ?', (curr_result,))
        connection.commit()
        return True
    except:
        return False







