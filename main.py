import os
from dotenv import load_dotenv
import telebot
from telebot import types
import sqlite3
import re
import logging




# загружаем ключ
load_dotenv('.env')
bot = telebot.TeleBot(os.getenv('TOKEN'))
db = sqlite3.connect('/home/artem/PycharmProjects/utv/db.sqlite3', check_same_thread=False)
cur = db.cursor()


@bot.message_handler(commands=['start'])
def send_welcome(message):
    markup = types.InlineKeyboardMarkup()
    buttonA = types.InlineKeyboardButton('Войти', callback_data='login')
    markup.add(buttonA)
    bot.send_message(message.chat.id, "Тест кнопок", reply_markup=markup)


@bot.callback_query_handler(func=lambda c: c.data == 'login')
def login(call):
    id = call.from_user.id
    res = cur.execute("SELECT telegram_id FROM utv_api_customuser WHERE telegram_id='%s'" % id)
    id_bd = res.fetchone()
    if id_bd:
        markup = types.InlineKeyboardMarkup()
        b_cards = types.InlineKeyboardButton('Мои активные карточки', callback_data='cards')
        markup.add(b_cards)
        bot.send_message(call.message.chat.id, f'Вы вошли {call.from_user.username}', reply_markup=markup)
    else:
        bot.send_message(call.message.chat.id, 'Добавьте свой ID на сайте')


@bot.callback_query_handler(func=lambda c: c.data == 'cards')
def cards(call):
    id = call.from_user.id
    res = cur.execute(
        "SELECT utv_api_cards.id, title FROM utv_api_cards "
        "LEFT JOIN utv_api_customuser "
        "ON utv_api_customuser.id=utv_api_cards.author_id "
        "WHERE utv_api_customuser.telegram_id='%s'" % id)
    cards = res.fetchall()
    markup = types.InlineKeyboardMarkup()
    list_btn = []
    for i in cards:
        title = i[1]
        id = i[0]
        list_btn.append(types.InlineKeyboardButton(f'{title}', callback_data=f'cards/{id}/'))
    markup.add(*list_btn)
    logging.info(f'Получил список карточек')
    bot.send_message(call.message.chat.id, 'Вот ваши созданные карточки', reply_markup=markup)

@bot.callback_query_handler(func=lambda c: 0 < len(re.findall(r'cards\/\d{1,}\/', c.data)))
def cards_detail(call):
    # Обрабатываем кнопку пользователя
    id_card = re.findall(r'\d{1,}', call.data)
    res = cur.execute("SELECT * FROM utv_api_cards "
                      "WHERE id='%s'" % int(id_card[0]))
    card = res.fetchone()
    title = card[1]
    description = card[2]
    created = card[3]
    deadline = card[4]
    text = f'Название: {title},\nОписание: {description},\nДата создания: {created},\nДедлайн: {deadline}'
    # Создаём кнопки
    list_btn = []
    markup = types.InlineKeyboardMarkup()
    res2 = cur.execute("SELECT * FROM utv_api_tableproject "
                       "LEFT JOIN utv_api_tablecards "
                       "ON utv_api_tableproject.id=utv_api_tablecards.table_id "
                       "WHERE utv_api_tablecards.table_id='%s'" % int(id_card[0]))
    table = res2.fetchall()
    for i in table:
        id = i[0]
        created = i[24]
        list_btn.append(types.InlineKeyboardButton(f'Таблица от {created}', callback_data=f'table/{id}/'))
    markup.add(*list_btn)
    bot.send_message(call.message.chat.id, text, reply_markup=markup)


@bot.callback_query_handler(func=lambda c: 0 < len(re.findall(r'table\/\d{1,}\/', c.data)))
def table_detail(call):
    id_table = re.findall(r'\d{1,}', call.data)
    res = cur.execute("SELECT * FROM utv_api_tableproject "
                      "WHERE id='%s'" % int(id_table[0]))
    table = res.fetchone()
    txt = []
    price_client = f'Цена для клиента: {table[1]}'
    txt.append(price_client)
    planned_cost = f'Плановая себестоимость: {table[2]}'
    txt.append(planned_cost)
    cost = f'Cебестоимость: {table[3]}'
    txt.append(cost)
    planned_salary = f'Плановая зарплата сотрудникам: {table[4]}'
    txt.append(planned_salary)
    salary = f'Зарплата сотрудника: {table[5]}'
    txt.append(salary)
    planned_actors_salary = f'Плановая зарплата актёрам: {table[6]}'
    txt.append(planned_actors_salary)
    actors_salary = f'Зарплата актёрам: {table[7]}'
    txt.append(actors_salary)
    planned_taxex_FOT = f"Плановые налоги ФОТ: {table[8]}"
    txt.append(planned_taxex_FOT)
    taxes_FOT = f"Налоги ФОТ: {table[9]}"
    txt.append(taxes_FOT)
    planned_other_express = f'Плановые Покупка реквизита для организации съемочного процесса непредвиденные расходы: {table[10]}'
    txt.append(planned_other_express)
    other_express = f'Плановые Покупка реквизита для организации съемочного процесса непредвиденные расходы: {table[11]}'
    txt.append(other_express)
    planned_buying_music = f'Плановая покупка музыки: {table[12]}'
    txt.append(planned_buying_music)
    buying_music = f'Покупка музыки: {table[13]}'
    txt.append(buying_music)
    planned_travel_expenses = f'Плановые командировачные расходы: {table[14]}'
    txt.append(planned_travel_expenses)
    travel_expenses = f'Фактические командировачные расходы: {table[15]}'
    txt.append(travel_expenses)
    planned_fare = f'Плановые транспортные расходы: {table[16]}'
    txt.append(planned_fare)
    fare = f'Tранспортные расходы: {table[17]}'
    txt.append(fare)
    planned_general_express = f'Плановые общехозяйственные расходы: {table[18]}'
    txt.append(planned_general_express)
    general_express = f'Общехозяйственные расходы: {table[19]}'
    txt.append(general_express)
    planned_profit = f'Плановая прибыль: {table[20]}'
    txt.append(planned_profit)
    profit = f'Прибыль: {table[21]}'
    txt.append(profit)
    planned_profitability = f'Плановая рентабельность: {table[22]}'
    txt.append(planned_profitability)
    profitability = f'Рентабельность: {table[23]}'
    txt.append(profitability)
    created = f'Созданно: {table[24]}'
    txt.append(created)
    update = f'Обновлена: {table[25]}'
    txt.append(update)
    # Посмотри созданные excel
    res2 = cur.execute("SELECT * FROM utv_api_tableexcel "
                       "WHERE table_id='%s'" % int(id_table[0]))
    list_btn = []
    for i in res2.fetchall():
        list_btn.append(types.InlineKeyboardButton(f'{i[1]}', callback_data=f'excel/{i[0]}/'))
    markup = types.InlineKeyboardMarkup()
    markup.add(*list_btn)
    bot.send_message(call.message.chat.id, ',\n'.join(txt), reply_markup=markup)


bot.infinity_polling()
