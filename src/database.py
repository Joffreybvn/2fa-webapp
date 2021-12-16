import base64
import binascii
from dataclasses import dataclass
from typing import Iterable, Union, Dict, Optional, Tuple
import boto3
import pyotp
from pyotp import OTP, TOTP, HOTP
from .config import config


dynamo_db = boto3.client(
    'dynamodb',
    region_name=config.aws_region_name,
    aws_access_key_id=config.aws_access_key,
    aws_secret_access_key=config.aws_access_key_secret,
)


class Logo:

    # Default placeholder
    _default = "placeholder"

    # Logo list
    _logos: Dict[str, str] = {
        'facebook': ''
    }

    @classmethod
    def get(cls, website) -> Optional[str]:
        return cls._logos.get(website, cls._default)


@dataclass
class OTPAuthenticator:
    otp: Union[OTP, TOTP, HOTP]
    image: str

    def __setattr__(self, name, value):

        # Override image value, append the full path to the image
        if name == 'image':
            value = f"./static/logos/{value}.png"
        self.__dict__[name] = value


class Database:

    def __init__(self):
        self.data = dict(self._load_all_data())

    @staticmethod
    def _load_all_data() -> Iterable[Tuple[str, OTPAuthenticator]]:
        """Load and yield all Authenticator entries from the database."""

        # Query all entries from the database
        response = dynamo_db.scan(
            TableName=config.dynamo_table_name,
            Select='ALL_ATTRIBUTES'
        )

        # Transform and yield OPTAuthenticator object
        if response['ResponseMetadata']['HTTPStatusCode'] == 200:
            for item in response['Items']:
                password = pyotp.parse_uri(item['otp_uri']['S'])
                logo = Logo.get(password.issuer)

                yield password.secret, OTPAuthenticator(otp=password, image=logo)

    @staticmethod
    def _is_valid_base32_digit(base32_string: str) -> bool:
        """Check if the given string is a valid base32 digit."""
        try:
            base64.b32decode(base32_string, casefold=True)
            return True
        except binascii.Error as error:
            print('Non-base32 digit found')
            return False

    def add(self, otp_uri: str):
        """Add a new Authenticator."""
        # Create an OTP object
        password = pyotp.parse_uri(otp_uri)

        # Check if the given secret is a correct and doesn't exist yet
        if self._is_valid_base32_digit(password.secret) and password.secret not in self.data:
            logo = Logo.get(password.issuer)

            # Update remotely
            response = dynamo_db.put_item(
                TableName=config.dynamo_table_name,
                Item={
                    config.dynamo_partition_key: {"S": password.secret},
                    "otp_uri": {"S": otp_uri}
                }
            )

            # Update locally
            if response['ResponseMetadata']['HTTPStatusCode'] == 200:
                self.data[password.secret] = OTPAuthenticator(
                    otp=password,
                    image=logo
                )

    def delete(self, secret_id: str):
        """Remove an authenticator"""

        # Delete from the database
        response = dynamo_db.delete_item(
            TableName=config.dynamo_table_name,
            Key={
                config.dynamo_partition_key: {"S": secret_id},
            }
        )

        # Delete locally:
        if response['ResponseMetadata']['HTTPStatusCode'] == 200:
            del self.data[secret_id]

    def __iter__(self) -> Iterable[OTPAuthenticator]:

        try:
            for entry in self.data.values():
                yield entry

        # Avoid throwing an error when 'self.data' changes.
        # Dict modification occurs when an authentication is deleted.
        except RuntimeError as exception:
            pass
