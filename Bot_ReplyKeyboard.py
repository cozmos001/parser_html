import telebot
from telebot import types
from parse_whith_search import parser
import glob
import os

TOKEN = 'token'
bot = telebot.TeleBot(TOKEN, parse_mode=None)


def buttons_menu():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    button_parse_all = types.KeyboardButton('Парсим все новости 📝')
    button_parse_search = types.KeyboardButton('Парсим по слову 📝')
    button_info = types.KeyboardButton('Инфо ℹ️')
    markup.add(button_parse_all, button_parse_search, button_info)
    return markup


def buttons_yes_no():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    button_yes = types.KeyboardButton('Да ✅')
    button_no = types.KeyboardButton('Нет ❌')
    markup.add(button_yes, button_no)
    return markup


@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    markup = buttons_menu()
    if message.text == '/start':
        msg = f'Привет {message.from_user.first_name}' \
              f'Выберете пункт меню 👇'
        bot.send_message(message.chat.id, text=msg, reply_markup=markup, parse_mode='HTML')
    elif message.text == '/help':
        msg = 'Это бот-парсер новостей с сайта pythondigest.ru\n' \
              'Для более подробной информации нажмите <b>Инфо</b>\n' \
              'Выберете пункт меню 👇'
        bot.send_message(message.chat.id, text=msg, reply_markup=markup, parse_mode='HTML')


@bot.message_handler(content_types=['text'])
def answer(message):
    if message.chat.type == 'private':

        if message.text == 'Парсим все новости':
            bot.send_message(message.chat.id, 'Парсинг начался это займет примерно 22-25 минут\n'
                                              'Наберитесь терпения 😁',
                             reply_markup=types.ReplyKeyboardRemove())
            bot.send_message(message.chat.id, '⏳')
            parser()
            markup = buttons_yes_no()
            bot.send_message(message.chat.id, 'Хотите получить файл?', reply_markup=markup)
            bot.register_next_step_handler(message, get_file)

        elif message.text == 'Парсим по слову':
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
            back = types.KeyboardButton('Назад ⬅️', )
            markup.add(back)
            bot.send_message(message.chat.id, "Отправьте слово которое должно быть в новости:", reply_markup=markup)
            bot.register_next_step_handler(message, search)

        elif message.text == 'Инфо ℹ️':
            bot.send_message(message.chat.id,
                             'Это бот который парсит новости с сайта\npythondigest.ru\n\n'
                             'При выборе - <b>"Парсим все новости"</b>,\n'
                             'Бот начнет парсинг всех новостей на сайте.\n\n'
                             'При выборе - <b>"Парсим по слову"</b>\n'
                             'Вам будет предложено отправить слово,\n'
                             'которое должно содержаться в новости.\n\n'
                             'После парсинга сформируется csv файл\n'
                             'в котором будет дата новости, заголовок\n'
                             'описание и ссылка на новость.\n'
                             'Далее вам будет предложено получить файл.\n\n'
                             'Файл не хранится на сервере,\n'
                             'Независимо от того что вы выберете\n'
                             '<b>Да</b> или <b>Нет</b> после он удаляется.',
                             parse_mode='HTML')

        else:
            bot.send_message(message.chat.id, 'Неизвестная команда, '
                                              'пожалуйста выберите пункт меню 👇')


def search(message):
    if message.text == 'Назад ⬅️':
        markup = buttons_menu()
        bot.send_message(message.chat.id, text='Выберите пункт меню 👇', reply_markup=markup)
    else:
        word_for_search = message.text
        bot.send_message(message.chat.id, 'Парсинг начался это займет какое-то время\n'
                                          'Наберитесь терпения 😁',
                         reply_markup=types.ReplyKeyboardRemove())
        bot.send_message(message.chat.id, '⏳')
        parser(word_for_search)
        markup = buttons_yes_no()
        bot.send_message(message.chat.id, 'Хотите получить файл?', reply_markup=markup)
        bot.register_next_step_handler(message, get_file)


def get_file(message):
    filename = glob.glob('*.csv')[0]
    if message.text == 'Да ✅':
        with open(filename, 'r') as file:
            bot.send_document(message.chat.id, file)
    os.remove(filename)
    markup = buttons_menu()
    bot.send_message(message.chat.id, text='Начнем новый парсинг\n'
                                           'Выберите пункт меню 👇', reply_markup=markup)


bot.infinity_polling()
