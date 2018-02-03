from bot.models import Action
from django.db.utils import IntegrityError


def action_edit(action, post_dict):
    error = False
    error_message = ''

    if 'text' in post_dict:
        text = post_dict['text']
        if text != '':
            action.text = text
        else:
            error = True
            action += 'Text field is empty\n'
    else:
        error = True
        action += 'Text field is not specified\n'

    if 'type_id' in post_dict:
        type_id = post_dict['type_id']
        if type_id != '':
            action.type_id = type_id
        else:
            error = True
            action += 'Type_id field is empty\n'
    else:
        error = True
        action += 'Type_id field is not specified\n'

    if error:
        return False, error_message
    else:
        result, error_message = _save(action)
        if result:
            return action, error_message
        else:
            return False, error_message


def action_add(post_dict):
    action = Action()
    error = False
    error_message = ''

    if 'text' in post_dict:
        text = post_dict['text']
        if text != '':
            action.text = text
        else:
            error = True
            action += 'Text field is empty\n'
    else:
        error = True
        action += 'Text field is not specified\n'

    if 'type_id' in post_dict:
        type_id = post_dict['type_id']
        if type_id != '':
            action.type_id = type_id
        else:
            error = True
            action += 'Type_id field is empty\n'
    else:
        error = True
        action += 'Type_id field is not specified\n'

    if error:
        return False, error_message
    else:
        result, error_message = _save(action)
        if result:
            return action, error_message
        else:
            return False, error_message


def _save(action):
    try:
        action.save()
        return action, None
    except IntegrityError:
        return False, 'Not unique type'