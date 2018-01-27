from config import token
from django.conf.urls import url
from bot.views import *


urlpatterns = [
    url(r'^' + token + '$', webhook, name='webhook'),
]
