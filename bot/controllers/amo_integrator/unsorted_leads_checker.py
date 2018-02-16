from time import time
from urllib.parse import urlencode

import requests
from bot.controllers.amo_integrator.leads import update_lead
from bot.controllers.amo_integrator.utils import authorize
from bot.models import User
from config import amo_user_host, amo_api_incoming_leads, amo_user_hash, amo_user_login, amo_chat_code, \
    amo_api_incoming_leads_accept, amo_api_leads


def _get_unsorted_leads():
    url = amo_user_host + amo_api_incoming_leads + '?api_key=%s' % amo_user_hash + '&login=%s' % amo_user_login
    cookies = authorize()
    r = requests.get(url, cookies=cookies)
    print(r.json())
    return r.json()['_embedded']['items']


def _accept(unsorted_lead):
    print(unsorted_lead)
    if unsorted_lead['category'] == 'chat' and unsorted_lead['incoming_lead_info']['service'] == amo_chat_code:
        user = User.objects.get(id=unsorted_lead['incoming_lead_info']['name'].split('.')[-1])
        lead_id = _accept_uid(unsorted_lead['uid'])
        _transfer_lead(lead_id, user)


def _transfer_lead(lead_id, user):
    user.lead_id = lead_id
    user.save()
    update_lead(user)


def _accept_uid(uid):
    url = amo_user_host + amo_api_incoming_leads_accept + '?api_key=%s&login=%s' % (amo_user_hash, amo_user_login)
    print(url)
    data = 'accept%5B0%5D=' + uid + '&user_id=2093440&status_id=18324790'
    headers = {"Accept": "application/json",
               'User-Agent': 'amoCRM-API-client/1.0',
               'Content-Type': 'application/x-www-form-urlencoded'}
    r = requests.post(url, data=data, headers=headers)
    return r.json()['data'][uid]['leads'][0]


def run_check():
    unsorted_list = _get_unsorted_leads()
    for unsorted in unsorted_list:
        _accept(unsorted)
