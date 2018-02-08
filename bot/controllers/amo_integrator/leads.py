from bot.models import User
from config import pipeline_id


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
                }

            ]
        }]
    }


def _get_user(contact):
    user_id = contact['name'].split('.')[1]
    return User.objects.get(id=user_id)