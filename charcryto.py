from django.db import models
from cryptography.fernet import Fernet
from django.conf import settings



class TrosgateCharField(models.CharField):
    '''
    # Define your model fields to look like below for charfield
        api_key1 = EncryptedCharField(max_length=100)
        api_key2 = EncryptedCharField(max_length=150)
    '''
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._key = None

    @property
    def key(self):
        if self._key is None:
            self._key = Fernet(settings.SECRET_KEY.encode())
        return self._key

    def from_db_value(self, value, expression, connection):
        if value is None:
            return value
        try:
            return self.key.decrypt(value.encode()).decode()
        except (AttributeError, ValueError):
            # Return the value as is if the key is not set or has been changed
            return value

    def to_python(self, value):
        if isinstance(value, str):
            return value
        if value is None:
            return value
        try:
            return self.key.decrypt(value.encode()).decode()
        except (AttributeError, ValueError):
            # Return the value as is if the secret key in settings is not set or has been changed
            return value

    def get_prep_value(self, value):
        if value is None:
            return value
        try:
            return self.key.encrypt(value.encode()).decode()
        except (AttributeError, ValueError):
            # Return the value as is if the key is not set or has been changed
            return value
