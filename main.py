import telebot
from dotenv import load_dotenv
import os
from data import open_data, save_data
from info import PLOT, GREETING, HELP

load_dotenv()
bot = telebot.TeleBot(os.getenv('TOKEN'))


# Отправляет описание локаций, добавляет кнопки с вариантами ответа
def ask_about_location(message, location):
    # открываем файл с локациями
    locations = open_data('location.json')

    # клавиатура
    markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)

    for answer in locations[location]['action']:
        markup.add(answer)

    # отправляет фото и описание локации
    bot.send_photo(message.chat.id, locations[location]['picture'],
                   reply_markup=telebot.types.ReplyKeyboardRemove())
    bot.send_message(message.chat.id, locations[location]['description'], reply_markup=markup)

    # Проверяет, является ли локация финальной
    if locations[location]['win'] != 0:
        ask_results(message, location)


# выводит концовку, удаляет кнопки
def ask_results(message, location):
    locations = open_data('location.json')

    bot.send_message(message.chat.id, locations[location]['win'], reply_markup=telebot.types.ReplyKeyboardRemove())


@bot.message_handler(commands=['start'])
def say_start(message):
    # клавиатура
    markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)

    markup.add('Приступим', '/help')

    bot.send_message(message.chat.id, GREETING, reply_markup=markup)

    data = open_data('users_data.json')

    data[message.chat.id] = None

    save_data(data)


@bot.message_handler(commands=['help'])
def say_help(message):
    bot.send_message(message.chat.id, HELP)


# обрабатывает ответ
@bot.message_handler(func=lambda message: True)
def accept_the_answer(message):
    msg = message.text

    if msg == 'Приступим':

        data = open_data('users_data.json')

        chat_id = str(message.chat.id)

        ask_about_location(message, 'start')

        data[chat_id] = 'start'

        save_data(data)

    elif msg in list(PLOT.keys()):

        data = open_data('users_data.json')

        chat_id = str(message.chat.id)

        ask_about_location(message, PLOT[msg])

        data[chat_id] = PLOT[msg]

        save_data(data)

    else:
        bot.send_message(message.chat.id, 'Воспользуйтесь кнопками.')


bot.polling()
