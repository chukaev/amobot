from bot.models import User
from config import amo_api_leads, amo_user_host
import requests
from .utils import authorize
from time import time
from bot.models import Price


def update_lead(user, need_price = False):
    price = Price.objects.get(id=1)
    data = {
        'update': [
            {
                'id': user.lead_id,
                # 'sale': str(price.value),
                'updated_at': str(int(time()) + 3600 * 4),
                # 'pipeline_id': str(18324790),
                'custom_fields': [
                    {
                        'id': 1774321,
                        'values': [
                            {
                                'value': user.country
                            }
                        ]
                    },
                    {
                        'id': 1772733,
                        'values': [
                            {
                                'value': user.city
                            }
                        ]
                    },
                    {
                        'id': 1774323,
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
    # if need_price:
    #     data['update'][0]['sale'] = str(price.value)
    cookies = authorize()
    url = amo_user_host + amo_api_leads
    r = requests.post(url, json=data, cookies=cookies)


def _get_user(contact):
    user_id = contact['name'].split('.')[1]
    return User.objects.get(id=user_id)