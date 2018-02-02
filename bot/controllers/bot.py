from bot import bot
from messages import *
from telebot import types
from config import main_domain
from django.urls import reverse


def existed_user_action(user, message):
    # if user.state == 1:
    #     main_menu_action(user, message) # Function to implement
    # user.save()
    if message.video or message.video_note or message.voice:
        markup = types.InlineKeyboardMarkup()
        pay = types.InlineKeyboardButton(text=pay_button_text, url=main_domain+reverse('payment')+'?id=%d&amount=1' % user.id)
        markup.add(pay)
        bot.send_message(user.id, after_video_message, reply_markup=markup)