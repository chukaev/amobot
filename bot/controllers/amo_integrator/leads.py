from bot.models import User
from config import pipeline_id, amo_api_leads, amo_user_host
import requests
from .utils import authorize


def create_lead(contact):
    user = _get_user(contact)
    data = {
        'add': [{
            'name': str(user.username),
            'status_id': 143,
            'pipeline_id': pipeline_id,
            'contact_id': contact['id'],
            'sale': 1000,
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
        }]
    }
    cookies = authorize()
    url = amo_user_host + amo_api_leads
    r = requests.post(url, json=data, cookies=cookies)
    print(r.text)


def _get_user(contact):
    user_id = contact['name'].split('.')[1]
    return User.objects.get(id=user_id)