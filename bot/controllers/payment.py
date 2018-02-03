from bot.models import User
from bot import bot
from messages import payment_get, amo_payment_get
from config import yandex_notification_secret as notification_secret
from bot.controllers.amo_integrator.api_requests import send_from_user
import hashlib


def proceed_payment(post_dict):
    status = check_valid(post_dict)
    if status:
        is_payed = post_dict['unaccepted'] == 'false'

        if is_payed:
            label = post_dict['label']
            user_id = label
            user = User.objects.filter(id=user_id).first()
            if user:
                amount = float(post_dict['withdraw_amount'])
                bot.send_message(user.id, payment_get % amount)
                send_from_user(user, amo_payment_get % amount)
        else:
            print('unaccepted')


def check_valid(post_dict):
    input_string = '%s&%s&%s&%s&%s&%s&%s&%s&%s' % (post_dict['notification_type'],
                                                   post_dict['operation_id'],
                                                   post_dict['amount'],
                                                   post_dict['currency'],
                                                   post_dict['datetime'],
                                                   post_dict['sender'],
                                                   post_dict['codepro'],
                                                   notification_secret,
                                                   post_dict['label'])
    sha1 = hashlib.sha1(input_string.encode('utf-8')).hexdigest()
    return sha1 == post_dict['sha1_hash']
