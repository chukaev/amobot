import json

from django.contrib.auth.decorators import login_required

from .handlers import * #it is needed for registering handlers

import telebot
from django.shortcuts import render, HttpResponse, redirect, get_object_or_404

from bot import bot
from bot.models import User, Action, Price
from config import *
from bot.controllers.payment import proceed_payment
from bot.controllers.amo_integrator.webhooks import proceed_update
from bot.controllers.action import action_edit
from bot.controllers.price import edit_price as price_edit


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
    proceed_update(update=request.POST)

    return HttpResponse(content="Ok", status=200)


def payment(request):
    print(10)
    get = request.GET
    if 'amount' in get and 'id' in get:
        amount = get['amount']
        user_id = get['id']
        user = get_object_or_404(User, id=user_id)
        error = None
        # if user.date_out >= datetime.now().date():
        #     error = True
        return render(request, 'payment.html', context={'amount': amount,
                                                        'id': user_id,
                                                        'error': error,
                                                        'yandex_money': yandex_money})
    else:
        error = 'Отсутствуют параметры'

    # else:
    #     year = int(Pricing.objects.get(id=YEAR_SUBSCRIBE_COST).value)
    #     semester = int(Pricing.objects.get(id=SEMESTER_SUBSCRIBE_COST).value)
    #     trimester = int(Pricing.objects.get(id=TRIMESTER_SUBSCRIBE_COST).value)
    #     month = int(Pricing.objects.get(id=MONTH_SUBSCRIBE_COST).value)
    #     return render(request, 'index.html', context={
    #             'year': year, 'semester': semester, 'trimester': trimester, 'month': month})


@login_required(login_url='login')
def action_list(request):
    actions = Action.objects.all()
    return render(request, "messages.html", context={'actions': actions})


@login_required(login_url='login')
def edit_action(request, action_id):
    action = get_object_or_404(Action, type_id=action_id)
    error_message = None
    if request.method == 'POST':
        status, error_message = action_edit(action, request.POST)
        if status:
            return redirect('action_list')
    return render(request, 'edit_message.html', context={'error': error_message, 'action': action})


@login_required(login_url='login')
def price_list(request):
    prices = Price.objects.all()
    return render(request, 'price_list.html', context={'prices': prices})


@login_required(login_url='login')
def edit_price(request, price_id):
    price = get_object_or_404(Price, id=price_id)
    error_message = None
    if request.method == 'POST':
        status, error_message = price_edit(price, request.POST)
    return redirect('price_list')


@login_required(login_url='login')
def index(request):
    return redirect('price_list')