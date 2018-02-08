from config import token
from django.conf.urls import url
from bot.views import *
from bot.models import TypeAction, ProblemAction


urlpatterns = [
    url(r'^' + token + '$', webhook, name='webhook'),

    url(r'file/(?P<file_id>.+)$', get_file, name='get_file'),
    url(r'amochat/' + 'test', amo_chat_webhook, name='amochat_webhook'),
    url(r'amochat/' + scope_id, amo_chat_webhook, name='amochat_webhook'),

    url(r'^types$', action_list, {'Type': TypeAction}, name='types_list'),
    url(r'^types/(?P<action_id>[0-9]+)/edit$', edit_action, {'Type': TypeAction}, name='edit_type_action'),
    url(r'^types/add$', add_action, {'Type': TypeAction}, name='add_type_action'),

    url(r'^problems$', action_list, {'Type': ProblemAction}, name='problem_list'),
    url(r'^problems/(?P<action_id>[0-9]+)/edit$', edit_action, {'Type': ProblemAction}, name='edit_problem_action'),
    url(r'^problems/add$', add_action, {'Type': ProblemAction}, name='add_problem_action'),

    url(r'^price$', price_list, name='price_list'),
    url(r'^price/(?P<price_id>[0-9]+)/edit$', edit_price, name='edit_price'),

    url(r'^question$', question_list, name='question_list'),
    url(r'^question/(?P<question_id>[0-9]+)/edit$', edit_question, name='edit_question'),

    url(r'amo/webhook$', amo_webhook, name='amo_webhook'),
    url(r'amo/webhook/delete$', amo_webhook, name='amo_delete_webhook'),

    url(r'^payment$', payment_webhook, name='payment_webhook'),

    url(r'$', index, name='index'),

]
