import os
import string
import re

ALPHABET = string.ascii_letters + string.digits
REGEXP = f'^[{re.escape(ALPHABET)}]+$'


class Config(object):
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URI')
    SECRET_KEY = os.getenv('SECRET_KEY')
