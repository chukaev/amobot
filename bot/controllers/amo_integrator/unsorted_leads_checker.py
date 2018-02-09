import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "amobot.settings")
django.setup()

from config import amo_user_host, amo_api_incoming_leads, amo_user_hash, amo_user_login, amo_chat_code, amo_api_incoming_leads_accept, amo_user_id, amo_api_leads, pipeline_id
from bot.controllers.amo_integrator.utils import authorize
from bot.models import User
import requests


def _get_unsorted_leads():
    url = amo_user_host + amo_api_incoming_leads + '?api_key=%s' % amo_user_hash + '&login=%s' % amo_user_login
    cookies = authorize()
    r = requests.get(url, cookies=cookies)
    print(r.json())
    return r.json()['_embedded']['items']


def _accept(unsorted_lead):
    if unsorted_lead['category'] == 'chat' and unsorted_lead['incoming_lead_info']['service'] == amo_chat_code:
        user = User.objects.get(id=unsorted_lead['incoming_lead_info']['name'].split('.')[-1])
        lead_id = _accept_uid(unsorted_lead['uid'])
        _transfer_lead(lead_id, user)


def _transfer_lead(lead_id, user):
    url = amo_user_host + amo_api_leads
    data = {
        'update': [
            {
                'id': lead_id,
                'sale': 1000,
                'pipeline_id': pipeline_id,
                'custom_fields': [
                    {
                        'id': '4399655',
                        'values': [
                            {
                                'value': user.city,
                                'subtype': 'city'
                            },
                            {
                                'value': user.country,
                                'subtype': 'country'
                            }
                        ]
                    },
                    {
                        'id': '1234567',
                        'values': [
                            {
                                'value': user.username,
                            },
                        ]
                    }
                ]
            }
        ]
    }
    cookies = authorize()
    r = requests.post(url, json=data, cookies=cookies)
    print(r.json())


def _accept_uid(uid):
    url = amo_user_host + amo_api_incoming_leads_accept + '?api_key=%s&login=%s' % (amo_user_hash, amo_user_login)
    print(url)
    data = {
        'accept': [uid],
        'user_id': amo_user_id,
        'status_id': 142
    }
    cookies = authorize()
    r = requests.post(url, json=data)
    print(r.json())
    return r.json()['data']['leads'][0]

if __name__ == '__main__':
    unsorted_list = _get_unsorted_leads()
    for unsorted in unsorted_list:
        _accept(unsorted)
