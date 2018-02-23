from django.shortcuts import get_object_or_404

from bot.models import TypeAction, ProblemAppearance


def appearance_edit(appearance, post_dict):
    error = False
    error_message = ''

    if 'text' in post_dict:
        text = post_dict['text']
        if text != '':
            appearance.text = text
        else:
            error = True
            error_message += 'Text field is empty\n'
    else:
        error = True
        error_message += 'Text field is not specified\n'

    if 'type_id' in post_dict:
        type_id = post_dict['type_id']
        type_action = TypeAction.objects.filter(id=type_id).first()
        if type_action:
            appearance.type_action = type_action
        else:
            error = True
            error_message += 'Type id field is wrong. Speak with developer'
    else:
        error = True
        error_message += 'Type_id field is not specified\n'

    if error:
        return False, error_message
    else:
        appearance.save()
        return appearance, error_message



def appearance_add(post_dict, problem_id):
    appearance = ProblemAppearance(problem_id=problem_id)
    error = False
    error_message = ''

    if 'text' in post_dict:
        text = post_dict['text']
        if text != '':
            appearance.text = text
        else:
            error = True
            error_message += 'Text field is empty\n'
    else:
        error = True
        error_message += 'Text field is not specified\n'

    if 'type_id' in post_dict:
        type_id = post_dict['type_id']
        type_action = TypeAction.objects.filter(id=type_id).first()
        if type_action:
            appearance.type_action = type_action
        else:
            error = True
            error_message += 'Type id field is wrong. Speak with developer'
    else:
        error = True
        error_message += 'Type_id field is not specified\n'

    if error:
        return False, error_message
    else:
        appearance.save()
        return appearance, error_message
