import os
import django
import sys
sys.path.append("~/amobot/")
print(os.getcwd())
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "amobot.settings")
django.setup()

from bot.controllers.amo_integrator.unsorted_leads_checker import run_check

run_check()