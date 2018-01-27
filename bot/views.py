from django.shortcuts import render, HttpResponse
from .handlers import * #it is needed for registering handlers
import json
import telebot
from bot import bot


def webhook(request):
    data = json.loads(request.body.decode('utf-8'))
    update = telebot.types.Update.de_json(data)
    bot.process_new_updates([update])
    return HttpResponse(content="Ok", status=200)
