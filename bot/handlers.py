from . import bot
from bot.controllers.bot import existed_user_action
from bot.controllers.user import get_user, new_user_action
from .utils import  to_main_page
from bot.controllers.amo_integrator.api_requests import send_to_amo
from bot.controllers.amo_integrator.leads import update_lead


@bot.message_handler(commands=['start'])
def handle_start(message):
    is_existed_user, user = get_user(message.from_user)
    if user.lead_id:
        update_lead(user)
    if is_existed_user:
        if user.state != 0:
            to_main_page(user)
        else:
            new_user_action(user)


@bot.message_handler(content_types=['text', 'audio', 'video', 'video_note', 'voice'])
def main_handler(message):
    is_existed_user, user = get_user(message.from_user)
    if user.lead_id:
        update_lead(user)
    print('send_to_amo')
    send_to_amo(user, message)
    if is_existed_user:
        existed_user_action(user, message)

#
# @bot.message_handler(content_types=['contact'])
# def contact_handler(message):
#     status, user = get_user(message.from_user)
#     user.phone = phone_format(message.contact.phone_number)
#     if user.state == 0:
#         user.state = 1
#         markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
#         yes_button = types.KeyboardButton('Да')
#         no_answer = types.KeyboardButton('Нет')
#         markup.add(yes_button, no_answer)
#         bot.send_message(user.id, 'Есть ли у вас ID пользователя-рефера?', reply_markup=markup)
#     else:
#         bot.send_message(user.id, 'Мы изменили ваш номер.')
#     user.save()
