from bot import bot


def send_to_amo(user, message):
    print(message.__dict__)
    print(message.video.__dict__)
    print(bot.get_file(message.video.file_id).__dict__)
