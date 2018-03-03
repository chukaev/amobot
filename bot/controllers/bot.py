from bot import bot
from messages import *
from telebot import types
from config import main_domain
from django.urls import reverse
from bot.models import Question, Price
from bot.utils import countries


def existed_user_action(user, message):
    # if user.state == 1:
    #     main_menu_action(user, message) # Function to implement
    # user.save()
    # if user.state == 1:
    #     choose_country(user, message)
    # elif user.state == 2:
    #     choose_city(user, message)
    if user.state >= 3:
        video_action(user, message)
    user.save()


def choose_country(user, message):
    country_try = message.text
    user.country = country_try
    user.state = 2
    bot.send_message(user.id, ask_for_city, reply_markup=types.ReplyKeyboardRemove())


def choose_city(user, message):
    if message.text != '':
        user.city = message.text
        user.state = 3
        bot.send_message(user.id, info_message)
        question = Question.objects.get(id=1)
        bot.send_message(user.id, question.text)
    else:
        bot.send_message(user.id, unknown_city)


def video_action(user, message):
    if user.state < 6:
        print('video')
        print(message.video_note)
        print(message.video)
        if message.video or message.video_note:
            question = Question.objects.get(id=user.state-1)
            bot.send_message(user.id, question.text)
            user.state += 1
    elif user.state == 6:
        if message.video or message.video_note:
            # price = Price.objects.get(id=1)
            # markup = types.InlineKeyboardMarkup()
            # pay = types.InlineKeyboardButton(text=pay_button_text,
            #                              url=main_domain + '?id=%d&amount=%.2f' % (user.id, price.value))
            # markup.add(pay)
            # bot.send_message(user.id, after_video_message % price.value, reply_markup=markup)
            bot.send_message(user.id, after_video_message)

            user.state = 8
