
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

    if error:
        return False, error_message
    else:
        action.save()
        return action, error_message
