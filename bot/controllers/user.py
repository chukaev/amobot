from bot.models import User, Question, StaticMessage
from telebot import types
from bot import bot
from messages import first_message, info_message
from django.core.exceptions import ObjectDoesNotExist
import json

def get_user(user):
    result = User.objects.filter(id=user.id).first()
    if result is None:
        result = _create_user(user)
        return False, result
    else:
        result.username = user.username
        return True, result


def _create_user(telegram_user):
    username = telegram_user.username
    if username == '':
        username = 'Пусто'
    user = User(id=telegram_user.id, first_name=telegram_user.first_name, username=username)
    new_user_action(user)
    user.save()
    return user


def new_user_action(user):
    # markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    # phone_button = types.KeyboardButton('Отправить номер телефона', request_contact=True)
    # markup.add(phone_button)
    # message = StaticMessage.objects.get(id=3)
    # buttons = generate_buttons(message.buttons)
    # bot.send_message(user.id, message.text, reply_markup=buttons)
    # question = Question.objects.get(id=1)
    # bot.send_message(user.id, question.text)
    message = StaticMessage.objects.get(id=1)
    buttons = generate_buttons(message.buttons)
    bot.send_message(user.id, message.text, reply_markup=buttons)


def get_user_from_amo_request(receiver):
    while len(receiver) > 4:
        try:
            user = User.objects.get(id=receiver)
            return user
        except ObjectDoesNotExist:
            receiver = receiver[:-1]
    return None


def generate_buttons(buttons):
    markup = types.InlineKeyboardMarkup()
    for key, value in json.loads(buttons).items():
        if key.startswith('http'):
            markup.add(types.InlineKeyboardButton(value, url=key))
        else:
            markup.add(types.InlineKeyboardButton(value, callback_data=key))
    return markup