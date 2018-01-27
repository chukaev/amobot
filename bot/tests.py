from django.test import TestCase
from mock import patch
from bot.models import User
from bot.utils import to_main_page, phone_format
import string
import random

def id_generator(size=6, chars=string.ascii_letters + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))

class TestTest(TestCase):
    def test_addition(self):
        self.assertEqual(2+2, 4)


class ToMainPageTests(TestCase):
    def setUp(self):
        User.objects.create(id=1234567, state=1)

    @patch('telebot.TeleBot.send_message')
    def test_main_page(self, send_message):
        user = User.objects.get(id=1234567)
        to_main_page(user)
        self.assertTrue(send_message.called)
        self.assertTrue(send_message.call_args[0][0] == user.id)
        self.assertTrue(send_message.call_args[0][1] == '✅')

    @patch('telebot.TeleBot.send_message')
    def test_main_page_with_message(self, send_message):
        user = User.objects.get(id=1234567)
        for _ in range(200):
            message = id_generator(random.randint(1, 2000))
            to_main_page(user, message)
            self.assertTrue(send_message.called)
            self.assertTrue(send_message.call_args[0][0] == user.id)
            self.assertTrue(send_message.call_args[0][1] == message, msg=message)


class PhoneFormatTests(TestCase):

    def test_phone_format(self):
        self.assertEqual(phone_format('01234567890'), '0-123-456-78-90')
        self.assertEqual(phone_format('001234567890'), '00-123-456-78-90')
        self.assertEqual(phone_format('+001234567890'), '+00-123-456-78-90')
