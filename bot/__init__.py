import telebot
from telegraph import Telegraph
from config import bot_token, telegraph_token


bot = telebot.TeleBot(bot_token)
telegraph = Telegraph(telegraph_token)