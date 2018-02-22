from bot.models import User, TypeAction, ProblemAction, StaticMessage
from bot import bot
import requests
from config import amo_user_host, amo_api_leads, amo_api_contact, bot_pipeline
from .utils import authorize


def proceed_update(update):
    lead = _get_lead(update)
    if lead:
        pipeline_id = lead['pipeline']['id']
        if pipeline_id == bot_pipeline:
            user = _get_user(lead)
            amo_type = _get_field(lead, 'ATYPE')[0]
            amo_problems = _get_field(lead, 'Травмы')
            action = TypeAction.objects.get(action_id=amo_type)
            problems = _get_problems(amo_problems)
            try:
                need_check = _get_field(lead, 'Проверка нужна?')[0]
            except IndexError:
                need_check = False
            send = False if need_check == '1' else user.send_review
            if send:
                # user.api_postfix += 1
                user.send_review = False
                user.save()
                hello_message = StaticMessage.objects.get(id=1)
                last_message = StaticMessage.objects.get(id=2)

                bot.send_message(user.id, hello_message.text, parse_mode='Markdown')
                bot.send_message(user.id, action.text, parse_mode='Markdown')
                for problem in problems:
                    bot.send_message(user.id, problem.text, parse_mode='Markdown')
                bot.send_message(user.id, last_message.text, parse_mode='Markdown')


def _get_user(lead):
    contact_id = lead['main_contact']['id']
    user_contact = _get_contact_details(contact_id)
    name = user_contact['name'].split('.')
    user_id = name[-1]
    user = User.objects.get(id=user_id)
    return user


def _get_lead(update):
    if 'leads[update][0][id]' in update:
        lead_id = update['leads[update][0][id]']
        lead = _get_lead_details(lead_id)
        return lead['_embedded']['items'][0]
    else:
        return None


def _get_lead_details(lead_id):
    cookies = authorize()
    url = amo_user_host + amo_api_leads + '?id=%s' % lead_id
    r = requests.get(url, cookies=cookies)
    return r.json()


def _get_contact_details(contact_id):
    cookies = authorize()
    url = amo_user_host + amo_api_contact + '?id=%s' % contact_id
    r = requests.get(url, cookies=cookies)
    return r.json()['_embedded']['items'][0]


def _get_field(lead, name):
    custom_fields = lead['custom_fields']
    result = []
    for field in custom_fields:
        if field['name'] == name:
            values = field['values']
            for val in values:
                result.append(val['value'])
    return result


def _get_problem_text(amo_problems):
    problems = _get_problems(amo_problems)
    result = '\n\n'
    for problem in problems:
        result += problem.text + '\n\n'
    return result


def _get_problems(amo_problems):
    result = []
    for amo_problem in amo_problems:
        try:
            problem = ProblemAction.objects.get(action_id=amo_problem)
            result.append(problem)
        except:
            pass
    return result

