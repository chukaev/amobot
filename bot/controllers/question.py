def question_edit(question, post_dict):
    error = False
    error_message = ''

    if 'text' in post_dict:
        text = post_dict['text']
        if text != '':
            question.text = text
        else:
            error = True
            error_message += 'Text field is empty\n'
    else:
        error = True
        error_message += 'Text field is not specified\n'

    question.save()

    if error:
        return False, error_message
    else:
        return question, error_message
