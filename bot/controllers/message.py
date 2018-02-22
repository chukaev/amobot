def message_edit(message, post_dict):
    error = False
    error_message = ''

    if 'text' in post_dict:
        text = post_dict['text']
        if text != '':
            message.text = text
        else:
            error = True
            message += 'Text field is empty\n'
    else:
        error = True
        message += 'Text field is not specified\n'

    if error:
        return False, message
    else:
        message.save()
    return message, message