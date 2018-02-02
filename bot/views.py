from django.shortcuts import render, HttpResponse, redirect
from .handlers import * #it is needed for registering handlers
import json
import telebot
from bot import bot
from config import *


def webhook(request):
    data = json.loads(request.body.decode('utf-8'))
    update = telebot.types.Update.de_json(data)
    bot.process_new_updates([update])
    return HttpResponse(content="Ok", status=200)


def get_file(request, file_id):
    url = telegram_file_link % (token, bot.get_file(file_id).file_path)
    return redirect(url)


def amo_webhook(request):
    print(request.body)
    data = json.loads(request.body.decode())
    bot.send_message(data['receiver'], data['text'])

