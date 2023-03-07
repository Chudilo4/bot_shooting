#!/usr/bin/python
import os
import telebot
from dotenv import load_dotenv
from telebot import types
import json
import requests

load_dotenv('../utv/.env')

API_TOKEN = os.getenv('BOT_TOKEN')

bot = telebot.TeleBot(API_TOKEN)


@bot.message_handler(commands=['start'])
def start(message):

    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton("👋 Поздороваться")
    markup.add(btn1)
    bot.send_message(message.from_user.id, "👋 Привет! Я твой бот-помошник!", reply_markup=markup)

@bot.message_handler(content_types=['text'])
def get_text_messages(message):

    if message.text == '👋 Поздороваться':
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True) #создание новых кнопок
        btn1 = types.KeyboardButton('Получить список пользователей')
        btn2 = types.KeyboardButton('Авторизоваться')
        markup.add(btn1, btn2)
        bot.send_message(message.from_user.id, '❓ Задайте интересующий вас вопрос', reply_markup=markup) #ответ бота
    elif message.text == 'Получить список пользователей':
        responsebot = ''
        response = requests.get(url='http://127.0.0.1:8000/api/v1/users/')
        txt = response.json()
        for i in txt:
            responsebot += f"{i.get('username')}" + '\n'
        bot.send_message(message.from_user.id, responsebot, parse_mode='Markdown')
    elif message.text == 'Авторизоваться':
        bot.send_message(message.from_user.id, str(bot.user.id), parse_mode='Markdown')



bot.polling(none_stop=True, interval=0) #обязательная для работы бота часть