import bot
from django.core.management.base import BaseCommand, CommandError

class Command(BaseCommand):
    help = 'Run bot polling'

    def handle(self, *args, **options):
        print("Polling bot")
        bot.bot.polling()
