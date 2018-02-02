from bot.models import User, Action
from bot import bot


def proceed_update(update):
    lead = _get_lead(update)
    if lead:
        user = _get_user(lead)
        amo_type = _get_type(lead)
        amo_problem = _get_problem(lead)
        action = Action.objects.get(amo_type)
        bot.send_message(user.id, action.text)


def _get_user(update):
    lead_id = _get_lead(update)
    lead = _get_lead_details(lead_id)
    user_contact = _get_contact_details(lead['_embedded']['items'][0]['id'])
    name = user_contact['_embedded']['items'][0]['name'].split('.')
    user_id = name[-1]
    user = User.objects.get(id=user_id)
    return user


def _get_lead(update):
    if 'leads[status][0][id]' in update:
        id = update['leads[status][0][id]']

    else:
        return None


