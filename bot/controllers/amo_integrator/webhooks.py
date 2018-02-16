from bot.models import User, TypeAction, ProblemAction
from bot import bot
import requests
from config import amo_user_host, amo_api_leads, amo_api_contact, bot_pipeline
from .utils import authorize


def proceed_update(update):
    lead = _get_lead(update)
    print(lead)
    if lead:
        print(lead)
        pipeline_id = lead['pipeline']['id']
        print(pipeline_id)
        if pipeline_id == bot_pipeline:
            user = _get_user(lead)
            amo_type = _get_field(lead, 'Тип')[0]
            amo_problems = _get_field(lead, 'Проблема')
            action = TypeAction.objects.get(action_id=amo_type)
            text_problems = _get_problem_text(amo_problems)
            print(3)
            try:
                need_check = _get_field(lead, 'Проверка нужна')[0]
            except IndexError:
                need_check = False
            print(10)
            send = True if user.send_review else need_check == '1'
            if send:
                user.api_postfix += 1
                user.send_review = False
                user.save()
                bot.send_message(user.id, action.text + text_problems)


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

