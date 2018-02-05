from bot.models import User, Action
from bot import bot
import requests
from requests.utils import dict_from_cookiejar
from config import amo_user_host, amo_api_leads, amo_api_auth, amo_api_contact, amo_user_login, amo_user_hash


def proceed_update(update):
    lead = _get_lead(update)
    if lead:
        user = _get_user(lead)
        amo_type = _get_field(lead, 'Тип')[0]
        amo_problems = _get_field(lead, 'Проблема')
        action = Action.objects.get(type_id=amo_type)
        text_problems = _get_problem_text(amo_problems)
        user.api_postfix += 1
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
    if 'leads[status][0][id]' in update:
        lead_id = update['leads[status][0][id]']
        lead = _get_lead_details(lead_id)
        return lead['_embedded']['items'][0]
    else:
        return None


def _get_lead_details(lead_id):
    cookies = _authorize()
    url = amo_user_host + amo_api_leads + '?id=%s' % lead_id
    r = requests.get(url, cookies=cookies)
    return r.json()


def _authorize():
    url = amo_user_host + amo_api_auth + '?type=json'
    data = {'USER_LOGIN': amo_user_login, 'USER_HASH': amo_user_hash}
    r = requests.post(url, data=data)
    return dict_from_cookiejar(r.cookies)


def _get_contact_details(contact_id):
    cookies = _authorize()
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
    result = '\n\nВаши проблемы:'
    for problem in amo_problems:
        result+= problem + ' '
    return result

