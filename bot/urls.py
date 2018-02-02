from config import token
from django.conf.urls import url
from bot.views import *


urlpatterns = [
    url(r'^' + token + '$', webhook, name='webhook'),

    url(r'file/(?P<file_id>.+)', get_file, name='get_file'),
    url(r'amochat/' + 'test', amo_chat_webhook, name='amochat_webhook'),
    url(r'amochat/' + scope_id, amo_chat_webhook, name='amochat_webhook'),

    url(r'amo/webhook', amo_webhook, name='amo_webhook'),

    url(r'', payment, name='payment'),

    url(r'^payment$', payment_webhook, name='payment_webhook'),
]
