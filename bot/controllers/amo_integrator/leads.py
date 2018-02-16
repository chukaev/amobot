from bot.models import User
from config import amo_api_leads, amo_user_host
import requests
from .utils import authorize
from time import time
from bot.models import Price


def update_lead(user):
    print(user.__dict__)
    price = Price.objects.get(id=1)
    data = {
        'update': [
            {
                'id': user.lead_id,
                'sale': str(price.value),
                'updated_at': str(int(time()) + 3600 * 4),
                # 'pipeline_id': str(18324790),
                'custom_fields': [
                    {
                        'id': 341835,
                        'values': [
                            {
                                'value': user.country
                            }
                        ]
                    },
                    {
                        'id': 341849,
                        'values': [
                            {
                                'value': user.city
                            }
                        ]
                    },
                    {
                        'id': 341851,
                        'values': [
                            {
                                'value': user.username
                            }
                        ]
                    }
                ]
            }
        ]
    }
    cookies = authorize()
    url = amo_user_host + amo_api_leads
    r = requests.post(url, json=data, cookies=cookies)
    print(r.text)


def _get_user(contact):
    user_id = contact['name'].split('.')[1]
    return User.objects.get(id=user_id)