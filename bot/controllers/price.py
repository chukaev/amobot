

def edit_price(price, post_dict):
    error = False
    message = ''

    if 'value' in post_dict:
        try:
            value = float(post_dict['value'])
            price.value = value
        except ValueError:
            error = True
            message += 'Value option is wrong\n'

    else:
        error = True
        message += 'Value option is not specified\n'
    if error:
        return False, message
    else:
        price.save()
        return price, message