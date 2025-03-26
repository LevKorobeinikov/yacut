import random
import re
import string
from datetime import datetime, timezone

from flask import url_for

from yacut import db
from yacut.constants import (
    BAD_NAME_SHORT_LINK, GENERATE_ERROR, LENGHT_SHORT,
    MAX_ATTEMPTS, MESSAGE_FOR_SHORT_LINK,
    ORIGINAL_MAX_LENGTH, REDIRECT_SHORT_URL,
    SHORT_MAX_LENGTH
)
from yacut.exceptions import ShortIdError

ALPHABET = string.ascii_letters + string.digits
REGEXP = f'^[{re.escape(ALPHABET)}]+$'


class URLMap(db.Model):
    """
    Модель для хранения ссылок.
    """
    id = db.Column(db.Integer, primary_key=True)
    original = db.Column(db.String(ORIGINAL_MAX_LENGTH), nullable=False)
    short = db.Column(db.String(SHORT_MAX_LENGTH), unique=True)
    timestamp = db.Column(
        db.DateTime,
        index=True,
        default=lambda: datetime.now(timezone.utc)
    )

    def to_dict(self):
        """
        Возвращает ссылку в виде JSON.
        """
        return dict(
            url=self.original,
            short_link=self.get_short_url(),
        )

    def get_short_url(self):
        """
        Расчёт урла коротюльки.
        """
        return url_for(REDIRECT_SHORT_URL, short=self.short, _external=True)

    @staticmethod
    def get_by_short_id(short):
        """
        Поиск ссылки по короткому идентификатору.
        """
        return URLMap.query.filter_by(short=short).first()

    @staticmethod
    def generate_short_id(
        original, length=LENGHT_SHORT, max_attempts=MAX_ATTEMPTS
    ):
        """
        Генерирует уникальный короткий идентификатор.
        Ограничивает число попыток во избежание бесконечного цикла.
        """
        for _ in range(max_attempts):
            short = ''.join(random.choices(ALPHABET, k=length))
            if not URLMap.get_by_short_id(short):
                return short
        raise RuntimeError(GENERATE_ERROR)

    @staticmethod
    def create(original, short=None):
        """
        Создаёт и сохраняет новую запись в БД.
        """
        if short:
            if len(short) > SHORT_MAX_LENGTH or not re.match(
                REGEXP, short
            ):
                raise ValueError(BAD_NAME_SHORT_LINK)
            if URLMap.get_by_short_id(short):
                raise ShortIdError(MESSAGE_FOR_SHORT_LINK)
        else:
            short = URLMap.generate_short_id(original)
        url_map = URLMap(original=original, short=short)
        db.session.add(url_map)
        db.session.commit()
        return url_map
