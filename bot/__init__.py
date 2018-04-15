import telebot
from telegraph import Telegraph
from config import bot_token, telegraph_token, webhook_url, webhook_ssl_cert
import time

bot = telebot.TeleBot(bot_token)
telegraph = Telegraph(telegraph_token)

#bot.remove_webhook()
#time.sleep(1)
#response = bot.set_webhook(url=webhook_url, certificate=open(webhook_ssl_cert, 'r'))
#print(response)
#print('Certificate is set on address: %s' % webhook_url)
