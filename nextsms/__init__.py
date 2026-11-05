import re
import sys
import requests
from base64 import b64encode
from typing import List, Dict, Union

_SENDER_ID = re.compile(r"^[A-Za-z0-9]{1,11}$")
_MSISDN = re.compile(r"^\d{10,15}$")
_MAX_TEXT = 1600
_BULK_KEYS = frozenset({"from", "to", "text"})
_ENDPOINTS = {
    False: (
        'https://messaging-service.co.tz/api/sms/v1/text/single',
        'https://messaging-service.co.tz/api/sms/v1/text/multi',
    ),
    True: (
        'https://messaging-service.co.tz/api/sms/v1/test/text/single',
        'https://messaging-service.co.tz/api/sms/v1/test/text/multi',
    ),
}


class NextSmsError(Exception):
    def __init__(self, message, status_code=None):
        super().__init__(message)
        self.status_code = status_code


class _Credentials:
    __slots__ = ("username", "_token")

    def __init__(self, username: str, token: str) -> None:
        self.username = username
        self._token = token

    def __repr__(self) -> str:
        return f"Credentials(username={self.username!r}, token='***')"

    @property
    def authorization(self) -> str:
        return f"Basic {self._token}"


class NextSms(object):

    SANDBOX_URL_SINGLE = _ENDPOINTS[True][0]
    SANDBOX_URL_MULTIPLE = _ENDPOINTS[True][1]
    PRODUCTION_URL_SINGLE = _ENDPOINTS[False][0]
    PRODUCTION_URL_MULTIPLE = _ENDPOINTS[False][1]

    Error = NextSmsError
    _sandbox = False

    def __init__(self, username: str = '', password: str = '', sandbox=False, timeout: float = 10) -> None:
        """Initialize nextsms access credentials

        Args:
            username (str): your username for nextsms
            password (str): your login password for nextsms
        """
        self.timeout = timeout
        self.sandbox = sandbox
        self._user = None
        if username or password:
            self.initialize(username, password)

    def __repr__(self) -> str:
        user = self._user.username if self._user else None
        return f"NextSms(username={user!r}, sandbox={self.sandbox!r})"

    @property
    def sandbox(self) -> bool:
        """Return the state of the sandbox environment whether its active or inactive

        Returns:
            bool: True if sandbox environment is active, False if not
        """
        return self._sandbox

    @sandbox.setter
    def sandbox(self, is_active: bool) -> None:
        """Set sandbox environment to active or inactive

        Args:
            is_active (bool): State of the sandbox environment (True|False)

        Raises:
            TypeError: If is_active is not of <class 'bool'>

        Example:
            >> import nextsms
            >> sender = nextsms('your username', 'your password')
            >> sender.sandbox = True 
        """
        if not isinstance(is_active, bool):
            raise TypeError(
                f"sandbox should of of type <class 'bool'> not {type(is_active)}")

        self._sandbox = is_active
        self.base_url_single, self.base_url_multiple = _ENDPOINTS[is_active]

    def initialize(self, username: str, password: str) -> None:
        """Initialize nextsms access credentials

        Args:
            username (str): your username for nextsms
            password (str): your login password for nextsms
        """
        self._user = self.create_user(username, password)

    def create_user(self, username: str, password: str) -> _Credentials:
        """Create user credentials.

        Args:
            username ([type]): username for nextms
            password ([type]): password for nextsms

        Raises:
            TypeError: if username in not of type <class 'str'>
            TypeError: if password in not of type <class 'str'>

        Returns:
            _Credentials: username plus the auth token
        """
        if not isinstance(username, str):
            raise TypeError(
                f"username should be of type <class 'str'> not {type(username)}")
        if not isinstance(password, str):
            raise TypeError(
                f"password should be of type <class 'str'> not {type(password)}")
        if username.strip() == "" or password == "":
            raise ValueError("username and password are required")
        if ":" in username or any(c in username or c in password for c in "\r\n"):
            raise ValueError("username and password have a bad character")
        token = b64encode(f'{username}:{password}'.encode()).decode()
        return _Credentials(username, token)

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
            'Authorization': self._user.authorization
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
            >> sender = nextsms('your username', 'your password')
            >> sender.sendsms('hello', '255700000000', 'NEXTSMS')
        """
        if not isinstance(sender_id, str) or _SENDER_ID.fullmatch(sender_id) is None:
            raise ValueError("sender_id should be 1 to 11 letters or digits")
        if not isinstance(message, str) or message.strip() == "" or len(message) > _MAX_TEXT:
            raise ValueError("message should be 1 to 1600 characters")
        if isinstance(recipients, str):
            if _MSISDN.fullmatch(recipients) is None:
                raise ValueError("recipient should be 10 to 15 digits")
            to = recipients
        elif isinstance(recipients, list) and recipients:
            to = []
            for item in recipients:
                if not isinstance(item, str) or _MSISDN.fullmatch(item) is None:
                    raise ValueError("recipient should be 10 to 15 digits")
                to.append(item)
        else:
            raise TypeError(
                f"recipient should be of type <class 'str'> or <class 'list'> not {type(recipients)}")

        return self._post(self.base_url_single, {
            'from': sender_id,
            'to': to,
            'text': message,
        })

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
            >> sender = nextsms('your username', 'your password')
            >> messages = [
                {'from':'NEXTSMS', 'to':'255700000000', 'text':'hello'},
                {'from':'NEXTSMS', 'to':'255711111111', 'text':'hello'}]           
            >> sender.send_bulk(messages)
        """
        if not isinstance(messages, list) or not messages:
            raise TypeError(
                f"messages should be of type <class 'list'> not type {type(messages)}")

        cleaned = []
        for index, item in enumerate(messages):
            if not isinstance(item, dict) or set(item) != _BULK_KEYS:
                raise ValueError(f"messages[{index}] should have from, to and text only")
            if not isinstance(item["from"], str) or _SENDER_ID.fullmatch(item["from"]) is None:
                raise ValueError("sender_id should be 1 to 11 letters or digits")
            if not isinstance(item["to"], str) or _MSISDN.fullmatch(item["to"]) is None:
                raise ValueError("recipient should be 10 to 15 digits")
            if not isinstance(item["text"], str) or item["text"].strip() == "" or len(item["text"]) > _MAX_TEXT:
                raise ValueError("message should be 1 to 1600 characters")
            cleaned.append({"from": item["from"], "to": item["to"], "text": item["text"]})

        return self._post(self.base_url_multiple, {'messages': cleaned})

    def _post(self, url, payload):
        try:
            response = requests.post(
                url,
                headers=self.create_header(),
                json=payload,
                timeout=self.timeout,
                verify=True,
                allow_redirects=False,
            )
        except requests.Timeout as exc:
            raise NextSmsError("NextSMS request timed out") from exc
        except requests.RequestException as exc:
            raise NextSmsError("NextSMS request failed") from exc
        if response.is_redirect or response.status_code >= 400:
            raise NextSmsError(
                f"NextSMS rejected the request (HTTP {response.status_code})",
                status_code=response.status_code,
            )
        try:
            body = response.json()
        except ValueError as exc:
            raise NextSmsError(
                f"NextSMS returned a non-JSON body (HTTP {response.status_code})",
                status_code=response.status_code,
            ) from exc
        if not isinstance(body, dict):
            raise NextSmsError("NextSMS returned an unexpected payload")
        return body


sys.modules[__name__] = NextSms
