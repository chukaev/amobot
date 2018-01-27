from . import bot
from telebot import types


def to_main_page(user, message='✅'):
    # Here should be your code of main page
    user.state = 1
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
    markup.add()
    bot.send_message(user.id, message, reply_markup=markup)
    user.save()


def phone_format(phone):
    return '%s-%s-%s-%s-%s' % (phone[:-10], phone[-10:-7], phone[-7:-4], phone[-4:-2], phone[-2:])