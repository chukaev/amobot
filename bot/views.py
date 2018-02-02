import json
from .handlers import * #it is needed for registering handlers

import telebot
from django.shortcuts import render, HttpResponse, redirect, get_object_or_404

from bot import bot
from bot.models import User
from config import *
from bot.controllers.payment import proceed_payment
from bot.controllers.amo_integrator import proceed_update


def webhook(request):
    data = json.loads(request.body.decode('utf-8'))
    update = telebot.types.Update.de_json(data)
    bot.process_new_updates([update])
    return HttpResponse(content="Ok", status=200)


def payment_webhook(request):
    if request.method == 'POST':
        print(request.POST)
        try:
            proceed_payment(request.POST)
        except Exception as e:
            import traceback
            traceback.print_exc()
            print(e)
        return HttpResponse(content="Ok", status=200)


def get_file(request, file_id):
    url = telegram_file_link % (token, bot.get_file(file_id).file_path)
    return redirect(url)


def amo_chat_webhook(request):
    data = json.loads(request.body.decode())
    bot.send_message(data['receiver'], data['text'])
    return HttpResponse(content="Ok", status=200)


def amo_webhook(request):
    print(request.POST)
    # if request.method == 'POST':
        # data = json.loads(request.body.decode())
        # proceed_update(data)
    return HttpResponse(content="Ok", status=200)


def payment(request):
    get = request.GET
    if 'amount' in get and 'months' in get and 'id' in get:
        amount = get['amount']
        user_id = get['id']
        user = get_object_or_404(User, id=user_id)
        error = None
        # if user.date_out >= datetime.now().date():
        #     error = True
    else:
        error = 'Отсутствуют параметры'
    return render(request, 'payment.html', context=
                {'amount': amount,
                    'id': user_id,
                    'error': error,
                    'yandex_money': yandex_money})
    # else:
    #     year = int(Pricing.objects.get(id=YEAR_SUBSCRIBE_COST).value)
    #     semester = int(Pricing.objects.get(id=SEMESTER_SUBSCRIBE_COST).value)
    #     trimester = int(Pricing.objects.get(id=TRIMESTER_SUBSCRIBE_COST).value)
    #     month = int(Pricing.objects.get(id=MONTH_SUBSCRIBE_COST).value)
    #     return render(request, 'index.html', context={
    #             'year': year, 'semester': semester, 'trimester': trimester, 'month': month})
