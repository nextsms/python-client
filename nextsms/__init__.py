import sys
import requests
from base64 import b64encode
from typing import List, Dict, Union
from collections import namedtuple


class NextSms(object):

    BASE_URL_SINGLE = 'https://messaging-service.co.tz/api/sms/v1/test/text/single'
    BASE_URL_MULTIPLE = 'https://messaging-service.co.tz/api/sms/v1/test/text/multi'

    User = namedtuple('User', 'username password secret_key')

    def __init__(self, username: str = '', password: str = '') -> None:
        """Initialize nextsms access credentials

        Args:
            username (str): your username for nextsms
            password (str): your login password for nextsms
        """
        self._user = (None
                      if not all(username and password)
                      else self.create_user(username, password))

    def initialize(self, username: str, password: str) -> None:
        """Initialize nextsms access credentials

        Args:
            username (str): your username for nextsms
            password (str): your login password for nextsms
        """
        self._user = self.create_user(username, password)

    def create_user(self, username: str, password: str) -> User:
        """Create a namedtuple of user credentials

        Args:
            username ([type]): username for nextms
            password ([type]): password for nextsms

        Raises:
            TypeError: if username in not of type <class 'str'>
            TypeError: if password in not of type <class 'str'>

        Returns:
            User: namedtuple datascture to hold user details (username, password, secret_key)
        """
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

    def create_header(self) -> Dict:
        """Auto generate json headers to be used in request

        Raises:
            Exception: If user credentials are not specified

        Returns:
            Dict: headers to be used on post requests
        """
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

    def sendsms(self, message: str, recipients: Union[str, List[str]], sender_id: str = "NEXTSMS") -> Dict:
        """Method to send sms using nextsms gateway

        Args:
            message (str): message to be sent 
            recipients (Union[str, List[str]]): A string of a single number or List of multiple recipients
            sender_id (str, optional): your Sender ID Defaults to "NEXTSMS".

        Raises:
            TypeError: If message is not type of <class 'str'>
            TypeError: If recipients is not type of <class 'str'> or <class 'list'>
            TypeError: If message is not type of <class 'str'>

        Returns:
            Dict: Response from the nextsms gateway

        Example:

            >> import nextsms 
            >> sender = nextsms('KalebuJordan', 'kalebu@opensource')
            >> sender.sendsms('hello', '255757294146', 'Neurotech')
        """
        if not isinstance(sender_id, str):
            raise TypeError(
                f"sender_id should of type <class 'str'> not {type(sender_id)}")
        if not isinstance(recipients, (str, list)):
            raise TypeError(
                f"recipient should be of type <class 'str'> or <class 'list'> not {type(recipients)}")
        if not isinstance(message, str):
            raise TypeError(
                f"message should be of type <class 'str'> not {type(message)}")

        return requests.post(
            self.BASE_URL_SINGLE,
            headers=self.create_header(),
            json={
                'from': sender_id,
                'to': recipients,
                'text': message
            }).json()

    def send_bulk(self, messages: List[Dict]) -> Dict:
        """[summary]

        Args:
            messages (List[Dict]): List of message objects to be sent 

        Raises:
            TypeError: if messages is not of type <class 'list'>

        Returns:
            Dict: NextSMS Response


        Example:

            >> import nextsms
            >> sender = nextsms('KalebuJordan', 'kalebu@opensource') 
            >> messages = [
                {'from':'NEXTSMS', 'to':'255757294146', 'text':'hello'},
                {'from':'NEXTSMS', 'to':'255754205561', 'text':'hello'}]           
            >> sender.send_bulk(messages)
        """
        if not isinstance(messages, list):
            raise TypeError(
                f"messages should be of type <class 'list'> not type {type(messages)}")

        return requests.post(
            self.BASE_URL_MULTIPLE,
            headers=self.create_header(),
            json={
                'messages': messages
            }
        ).json()


sys.modules[__name__] = NextSms
