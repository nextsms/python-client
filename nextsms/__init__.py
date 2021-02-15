import sys
import requests
from base64 import b64encode
from collections import namedtuple


class NextSms(object):

    BASE_URL = 'https://messaging-service.co.tz'

    User = namedtuple('User', 'username password secret_kery')

    def __init__(self, username: str, password: str) -> None:
        self._user = self.create_user(username, password)

    def create_user(self, username, password):
        if not isinstance(username, str):
            raise TypeError(
                f"username should be of type <class 'str'> not {type(username)}")
        if not isinstance(password, str):
            raise TypeError(
                f"password should be of type <class 'str'> not {type(password)}")
        return self.User(
            username=username,
            password=password,
            secret_key=b64encode(f'{username}:{password}'.encode()).decode()
        )

    def create_header(self):
        return {
            'Content-Type': 'json',
            'Authorization': f'Basic {self._user.secret_key}'
        }

    def send_sms(self):
        pass


sys.modules[__name__] = NextSms
