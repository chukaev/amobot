from config import token
from django.conf.urls import url
from bot.views import *


urlpatterns = [
    url(r'^' + token + '$', webhook, name='webhook'),

    url(r'file/(?P<file_id>.+)$', get_file, name='get_file'),
    url(r'amochat/' + 'test', amo_chat_webhook, name='amochat_webhook'),
    url(r'amochat/' + scope_id, amo_chat_webhook, name='amochat_webhook'),

    url(r'^actions$', action_list, name='action_list'),
    url(r'^actions/(?P<action_id>[0-9]+)/edit$', edit_action, name='edit_action'),
    url(r'^actions/add$', add_action, name='add_action'),

    url(r'^price$', price_list, name='price_list'),
    url(r'^price/(?P<price_id>[0-9]+)/edit$', edit_price, name='edit_price'),

    url(r'amo/webhook$', amo_webhook, name='amo_webhook'),

    url(r'', index, name='index'),

    url(r'^payment$', payment_webhook, name='payment_webhook'),
]
