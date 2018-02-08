from bot import bot
from messages import *
from telebot import types
from config import main_domain
from django.urls import reverse
from bot.models import Price


def existed_user_action(user, message):
    # if user.state == 1:
    #     main_menu_action(user, message) # Function to implement
    # user.save()

    if user.state == 1:
        choose_country(user, message)
    elif user.state == 2:
        choose_city(user, message)
    elif 3 <= user.state <= 6:
        video_action(user, message)
    
    if message.video or message.video_note or message.voice:
        markup = types.InlineKeyboardMarkup()
        price = Price.objects.get(id=1)
        pay = types.InlineKeyboardButton(text=pay_button_text, url=main_domain+'?id=%d&amount=%.2f' % (user.id, price.value))
        markup.add(pay)
        bot.send_message(user.id, after_video_message % price.value, reply_markup=markup)