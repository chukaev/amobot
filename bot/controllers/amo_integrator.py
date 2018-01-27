from bot import bot


def send_to_amo(user, message):
    print(message.__dict__)
    print(message.voice.__dict__)
    print(bot.get_file(message.voice.file_id).__dict__)
    file = bot.download_file(bot.get_file(message.voice.file_id))
    print(file.__dict__)
