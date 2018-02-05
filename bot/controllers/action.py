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

    if 'action_id' in post_dict:
        action_id = post_dict['action_id']
        if action_id != '':
            action.action_id = action_id
        else:
            error = True
            action += 'action_id field is empty\n'
    else:
        error = True
        action += 'action_id field is not specified\n'

    if error:
        return False, error_message
    else:
        result, error_message = _save(action)
        if result:
            return action, error_message
        else:
            return False, error_message


def action_add(post_dict, Type):
    action = Type()
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

    if 'action_id' in post_dict:
        action_id = post_dict['action_id']
        if action_id != '':
            action.action_id = action_id
        else:
            error = True
            action += 'action_id field is empty\n'
    else:
        error = True
        action += 'action_id field is not specified\n'

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