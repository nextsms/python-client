import sys
import requests
from base64 import b64encode
from typing import List, Dict
from collections import namedtuple


class NextSms(object):

    BASE_URL = ' https://messaging-service.co.tz/api/sms/v1/test/text/single'

    User = namedtuple('User', 'username password secret_key')

    def __init__(self) -> None:
        self._user = None

    def initialize(self, username: str, password: str) -> None:
        self._user = self.create_user(username, password)

    def create_user(self, username, password) -> User:
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
        if not self._user:
            raise Exception(
                '''
                Please Make sure You initialize before calling any other method
                
                >> import nextsms 
                >> nextsms.initialize(username, password)'''
            )

        return {
            'Accept': 'application/json',
            'Content-Type': 'application/json',
            'Authorization': f'Basic {self._user.secret_key}'
        }

    def send_sms(self, message: str, recipient: str, sender_id: str = "NEXTSMS"):
        if not isinstance(sender_id, str):
            raise TypeError(
                f"sender_id should of type <class 'str'> not {type(sender_id)}")
        if not isinstance(recipient, str):
            raise TypeError(
                f"recipient should be of type <class 'str'> not {type(recipient)}")
        if not isinstance(message, str):
            raise TypeError(
                f"message should be of type <class 'str'> not {type(message)}")

        return requests.post(
            self.BASE_URL,
            headers=self.create_header(),
            json={
                'from': sender_id,
                'to': recipient,
                'text': message
            }
        ).json()


sys.modules[__name__] = NextSms()
