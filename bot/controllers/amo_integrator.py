from bot import bot
from django.urls import reverse
import json
import requests
import time
from config import *
import hashlib
import hmac


def send_to_amo(user, message):
    print(message.from_user.__dict__)
    photos = bot.get_user_profile_photos(message.from_user.id).photos
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
    send_content(message, body)


def get_body_from_media(media):
    return main_domain + reverse('get_file', kwargs={'file_id': media.file_id})


def send_content(message, body):
    photos = bot.get_user_profile_photos(message.from_user.id).photos
    print(photos[0])
    data = {
        'event_type': 'new_message',
        'payload': {
            'timestamp': time.time(),
            'msgid': message.message_id,
            'conversation_id': message.from_user.id,
            'sender': {
                'id': message.from_user.id,
                'avatar': telegram_file_link % (token, bot.get_file(photos[0][3].file_id).file_path),
                'name': message.from_user.first_name,
            },
            'message': {
                'type': 'text',
                'text': body,
            }
        }
    }
    url = amo_chat_host + (amo_new_message_url % scope_id)
    payload = json.dumps(data)
    signature = hmac.new(amo_channel_secret.encode(), payload.encode(), 'sha1').hexdigest()
    headers = {'X-Signature': signature, 'Content-Type': 'application/json', 'Cache-Control': 'no-cache'}
    r = requests.post(url=url, data=payload, headers=headers)
    return r.text