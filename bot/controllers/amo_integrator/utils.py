from config import *
from requests.utils import dict_from_cookiejar
import requests


def authorize():
    url = amo_user_host + amo_api_auth + '?type=json'
    data = {'USER_LOGIN': amo_user_login, 'USER_HASH': amo_user_hash}
    r = requests.post(url, data=data)
    return dict_from_cookiejar(r.cookies)