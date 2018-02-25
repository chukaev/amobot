from . import bot
from telebot import types


def to_main_page(user, message='✅'):
    # Here should be your code of main page
    user.state = 3
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
    markup.add()
    bot.send_message(user.id, message, reply_markup=markup)
    user.save()


def phone_format(phone):
    return '%s-%s-%s-%s-%s' % (phone[:-10], phone[-10:-7], phone[-7:-4], phone[-4:-2], phone[-2:])


countries = {
    'россия': 'RU',
    'украина': 'UA',
    'грузия': 'GE',
    'белоруссия': 'BY',
    'казахстан': 'КZ'
}


def markup_for_country():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    for country, code in countries.items():
        markup.add(types.KeyboardButton(country))
    return markup
