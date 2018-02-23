import json

from django.contrib.auth.decorators import login_required

from bot.controllers.appearance import appearance_edit, appearance_add
from bot.controllers.message import message_edit
from .handlers import * #it is needed for registering handlers

import telebot
from django.shortcuts import render, HttpResponse, redirect, get_object_or_404

from bot import bot
from bot.models import User, TypeAction, Price, Question, StaticMessage, ProblemAction, ProblemAppearance
from config import *
from bot.controllers.payment import proceed_payment
from bot.controllers.amo_integrator.webhooks import proceed_update
from bot.controllers.action import action_edit, action_add
from bot.controllers.price import edit_price as price_edit
from bot.controllers.question import question_edit
from bot.controllers.user import get_user_from_amo_request


def webhook(request):
    data = json.loads(request.body.decode('utf-8'))
    update = telebot.types.Update.de_json(data)
    bot.process_new_updates([update])
    return HttpResponse(content="Ok", status=200)


def payment_webhook(request):
    print(request.POST)
    if request.method == 'POST':
        try:
            proceed_payment(request.POST)
        except Exception as e:
            import traceback
            traceback.print_exc()
            print(e)
        return HttpResponse(content="Ok", status=200)


def get_file(request, file_id):
    url = telegram_file_link % (bot_token, bot.get_file(file_id).file_path)
    return render(request, 'video_file.html', context={'url': url})


def amo_chat_webhook(request):
    data = json.loads(request.body.decode())
    user = get_user_from_amo_request(data['receiver'])
    if user:
        bot.send_message(user.id, data['text'])
    return HttpResponse(content="Ok", status=200)


def amo_webhook(request):
    # if request.method == 'POST':
        # data = json.loads(request.body.decode())
        # proceed_update(data)

    proceed_update(update=request.POST)

    return HttpResponse(content="Ok", status=200)


def payment(request):
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
def action_list(request, Type):
    actions = Type.objects.all()
    reurned_type = False
    if Type == TypeAction:
        reurned_type = True
    return render(request, "actions.html", context={'actions': actions, 'type': reurned_type})


@login_required(login_url='login')
def edit_action(request, action_id, Type):
    action = get_object_or_404(Type, id=action_id)
    error_message = None
    if request.method == 'POST':
        status, error_message = action_edit(action, request.POST)
        if status:
            print(Type.__class__)
            if Type.__class__ == TypeAction.__class__:
                return redirect('types_list')
            else:
                return redirect('problem_list')
    return render(request, 'edit_action.html', context={'error': error_message, 'action': action})


@login_required(login_url='login')
def add_action(request, Type):
    error_message = None
    if request.method == 'POST':
        status, error_message = action_add(request.POST, Type)
        if status:
            return redirect('index')
    return render(request, 'edit_action.html', context={'error': error_message})


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


@login_required(login_url='login')
def question_list(request):
    questions = Question.objects.all()
    return render(request, "questions.html", context={'questions': questions})


@login_required(login_url='login')
def edit_question(request, question_id):
    question = get_object_or_404(Question, id=question_id)
    error_message = None
    if request.method == 'POST':
        status, error_message = question_edit(question, request.POST)
        if status:
            return redirect('question_list')
    return render(request, 'edit_question.html', context={'error': error_message, 'question': question})


@login_required(login_url='login')
def messages_list(request):
    messages = StaticMessage.objects.all()
    return render(request, 'messages.html', context={
        'messages': messages
    })


@login_required(login_url='login')
def edit_message(request, message_id):
    message = get_object_or_404(StaticMessage, id=message_id)
    error_message = None
    if request.method == 'POST':
        status, error_message = message_edit(message, request.POST)
        if status:
            return redirect('static_messages')
    return render(request, 'edit_message.html', context={'error': error_message, 'message': message})


@login_required(login_url='login')
def problem_appearance(request, problem_id):
    problem = get_object_or_404(ProblemAction, id=problem_id)
    appearance = ProblemAppearance.objects.filter(problem=problem).all()
    return render(request, "appearance.html", context={'problem': problem, 'appearances': appearance})


@login_required(login_url='login')
def edit_appearance(request, appearance_id):
    appearance = get_object_or_404(ProblemAppearance, id=appearance_id)
    types = TypeAction.objects.all()
    error_message = None
    if request.method == 'POST':
        status, error_message = appearance_edit(appearance, request.POST)
        if status:
            return redirect('problem_appearance', appearance.problem.id)
    return render(request, 'edit_appearance.html', context={'types': types, 'error': error_message, 'appearance': appearance})


@login_required(login_url='login')
def add_appearance(request, problem_id):
    problem = get_object_or_404(ProblemAction, id=problem_id)
    types = TypeAction.objects.all()
    error_message = None
    if request.method == 'POST':
        status, error_message = appearance_add(request.POST, problem.id)
        if status:
            return redirect('problem_appearance', problem_id)
    return render(request, 'edit_appearance.html', context={'types': types, 'error': error_message})
