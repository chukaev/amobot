from bot import bot
from django.urls import reverse
import json
import requests
import time
from config import *
from config import api_implementation_version
import hmac


def send_to_amo(user, message):
    if message.text:
        body = message.text
    elif message.video:
        body = get_body_from_media(message.video)
    elif message.voice:
        body = get_body_from_media(message.voice)
    elif message.video_note:
        body = get_body_from_media(message.video_note)
    elif message.audio:
        body = get_body_from_media(message.audio)
    elif message.document:
        body = get_body_from_media(message.document)
    else:
        body = 'Unknown type, show this to administrator\n' + str(message.__dict__)
    res = send_content(user, message, body)



def get_body_from_media(media):
    return main_domain + reverse('get_file', kwargs={'file_id': media.file_id})


def send_from_user(user, body):
    photos = bot.get_user_profile_photos(user.id).photos
    data = {
        'event_type': 'new_message',
        'payload': {
            'timestamp': int(time.time()),
            'msgid': str(body+str(user.id)+str(int(time.time()))),
            'conversation_id': 'c' + str(user.id) + str(user.api_postfix),
            'sender': {
                'id': str(user.id) + str(api_implementation_version),
                'avatar': telegram_file_link % (token, bot.get_file(photos[0][2].file_id).file_path),
                'name': user.first_name.replace('.', '') + '.' + str(user.id),
            },
            'message': {
                'type': 'text',
                'text': body,
            }
        }
    }
    return send_data(data)


def send_content(user, message, body):
    photos = bot.get_user_profile_photos(message.from_user.id).photos
    data = {
        'event_type': 'new_message',
        'payload': {
            'timestamp': int(time.time()),
            'msgid': str(message.message_id),
            'conversation_id': 'c' + str(message.from_user.id) + str(user.api_postfix),
            'sender': {
                'id': str(message.from_user.id) + str(api_implementation_version),
                'avatar': telegram_file_link % (token, bot.get_file(photos[0][2].file_id).file_path),
                'name': message.from_user.first_name.replace('.', '') + '.' + str(message.from_user.id),
            },
            'message': {
                'type': 'text',
                'text': body,
            }
        }
    }
    return send_data(data)


def send_data(data):
    url = amo_chat_host + (amo_new_message_url % scope_id)
    payload = json.dumps(data)
    signature = hmac.new(amo_channel_secret.encode(), payload.encode(), 'sha1').hexdigest()
    headers = {'X-Signature': signature, 'Content-Type': 'application/json', 'Cache-Control': 'no-cache'}
    r = requests.post(url=url, data=payload, headers=headers)
    print(10)
    print(r.text)
    return r.text, data
