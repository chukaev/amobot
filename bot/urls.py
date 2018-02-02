from config import token
from django.conf.urls import url
from bot.views import *


urlpatterns = [
    url(r'^' + token + '$', webhook, name='webhook'),

    url(r'file/(?P<file_id>[0-9]+)', get_file, name='get_file'),
    url(r'amochat/' + 'test', amo_webhook, name='amo_webhook')
]
