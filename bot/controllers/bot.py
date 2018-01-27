from telebot import types
from tgBot import bot
from tgBot.utils import to_main_page, to_invest_page, to_ref_page, to_pay_page, change_payeer
from tgBot.models import *
from tgBot.check import run as run_payment_check
from messages import before_pay_message, ref_message, invest_message, success_registration
from config import payeer_account


def existed_user_action(user, message):
    if user.state == 1:
        main_menu_action(user, message) # Function to implement
    user.save()
