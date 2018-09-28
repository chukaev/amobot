from . import bot
from bot.controllers.bot import existed_user_action
from bot.controllers.user import get_user, new_user_action
from bot.controllers.amo_integrator.api_requests import send_to_amo
from bot.controllers.amo_integrator.leads import update_lead


@bot.message_handler(commands=['start'])
def handle_start(message):
    is_existed_user, user = get_user(message.from_user)
    if user.lead_id:
        update_lead(user)
    if is_existed_user:
        # user.state = 3
        new_user_action(user)
        user.save()


@bot.message_handler(content_types=['text', 'audio', 'video', 'video_note', 'voice'])
def main_handler(message):
    is_existed_user, user = get_user(message.from_user)
    if user.lead_id:
        update_lead(user)
    send_to_amo(user, message)
    if is_existed_user:
        existed_user_action(user, message)


@bot.inline_handler(lambda message: len(message.query) > 0)
def callback_handler(message):
    is_existed_user, user = get_user(message.from_user)
    if user.lead_id:
        update_lead(user)
    send_to_amo(user, message)
    if is_existed_user:
        existed_user_action(user, message)
