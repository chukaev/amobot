from telebot import types


def existed_user_action(user, message):
    if user.state == 1:
        main_menu_action(user, message) # Function to implement
    user.save()
