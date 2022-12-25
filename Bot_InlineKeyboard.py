import telebot
from telebot import types
from parse_whith_search import parser
import glob
import os

TOKEN = '5657912444:AAF777CZANjDhv0789WDPD0KCuvDAwHPRew'
bot = telebot.TeleBot(TOKEN, parse_mode=None)


def buttons_menu():
    markup = types.InlineKeyboardMarkup(row_width=1)
    button_parse_all = types.InlineKeyboardButton('Парсим все новости 📝', callback_data='parse_all')
    button_parse_search = types.InlineKeyboardButton('Парсим по слову 📝', callback_data='parse_search')
    button_info = types.InlineKeyboardButton('Инфо ℹ️', callback_data='info')
    markup.add(button_parse_all, button_parse_search, button_info)
    return markup


def buttons_yes_no():
    markup = types.InlineKeyboardMarkup(row_width=2)
    button_yes = types.InlineKeyboardButton('Да ✅', callback_data='yes')
    button_no = types.InlineKeyboardButton('Нет ❌', callback_data='no')
    markup.add(button_yes, button_no)
    return markup


@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    markup = buttons_menu()
    if message.text == '/start':
        msg = f'Привет {message.from_user.first_name}'
        bot.send_message(message.chat.id, text=msg, reply_markup=markup, parse_mode='HTML')
    elif message.text == '/help':
        msg = 'Это бот-парсер новостей с сайта pythondigest.ru \n' \
              'Для более подробной информации нажмите <b>Инфо</b> \n' \
              'Выберете пункт меню 👇'
        bot.send_message(message.chat.id, text=msg, reply_markup=markup, parse_mode='HTML')


@bot.callback_query_handler(func=lambda call: call.data == 'parse_all')
def callback_parse_all(call):
    bot.send_message(call.message.chat.id, 'Парсинг начался это займет '
                                           'примерно 22-25 минут\n'
                                           'Наберитесь терпения 😁')
    bot.send_message(call.message.chat.id, '⏳')
    parser()
    markup = buttons_yes_no()
    bot.send_message(call.message.chat.id, 'Хотите получить файл?', reply_markup=markup)


@bot.callback_query_handler(func=lambda call: call.data == 'parse_search')
def callback_parse_search(call):
    bot.clear_step_handler(call.message)
    markup = types.InlineKeyboardMarkup(row_width=2)
    beck = types.InlineKeyboardButton('Назад ⬅️', callback_data='back', )
    markup.add(beck)
    msg = bot.send_message(call.message.chat.id, "Отправьте слово которое должно быть в новости:", reply_markup=markup)
    bot.register_next_step_handler(msg, search)


def search(message):
    word_for_search = message.text
    bot.send_message(message.chat.id, 'Парсинг начался это займет какое-то время\n'
                                      'Наберитесь терпения 😁')
    bot.send_message(message.chat.id, '⏳')
    parser(word_for_search)
    markup = buttons_yes_no()
    bot.send_message(message.chat.id, 'Хотите получить файл?', reply_markup=markup)


@bot.callback_query_handler(func=lambda call: call.data == 'info')
def callback_info(call):
    bot.send_message(call.message.chat.id,
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

    markup = buttons_menu()
    bot.send_message(call.message.chat.id, text='Выберете пункт меню 👇', reply_markup=markup, parse_mode='HTML')


@bot.callback_query_handler(func=lambda call: call.data == 'back')
def callback_back(call):
    markup = buttons_menu()
    bot.send_message(call.message.chat.id, text='Выберете пункт меню 👇', reply_markup=markup, parse_mode='HTML')


@bot.callback_query_handler(func=lambda call: call.data == 'yes')
def callback_yes(call):
    filename = glob.glob('*.txt')[0]
    with open(filename, 'r') as file:
        bot.send_document(call.message.chat.id, file)
    os.remove(filename)
    markup = buttons_menu()
    bot.send_message(call.message.chat.id, text='Выберете пункт меню 👇', reply_markup=markup, parse_mode='HTML')


@bot.callback_query_handler(func=lambda call: call.data == 'no')
def callback_no(call):
    filename = glob.glob('*.txt')[0]
    os.remove(filename)
    markup = buttons_menu()
    bot.send_message(call.message.chat.id, text='Выберете пункт меню 👇', reply_markup=markup, parse_mode='HTML')


@bot.message_handler(content_types=['text'])
def text(message):
    bot.send_message(message.chat.id, 'Неизвестная команда')
    markup = buttons_menu()
    bot.send_message(message.chat.id, text='Выберете пункт меню 👇', reply_markup=markup, parse_mode='HTML')


bot.infinity_polling()
