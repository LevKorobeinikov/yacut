import random
from datetime import datetime
import re

from flask import url_for

from settings import ALPHABET, REGEXP
from yacut import db
from yacut.constants import (
    BAD_NAME_SHORT, GENERATE_ERROR, LENGHT_SHORT,
    MAX_ATTEMPTS, MESSAGE_FOR_SHORT,
    ORIGINAL_MAX_LENGTH, ORIGINAL_URL_LONG, REDIRECT_SHORT,
    SHORT_MAX_LENGTH
)
from yacut.exceptions import ShortError


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
        default=datetime.now
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
        return url_for(REDIRECT_SHORT, short=self.short, _external=True)

    @staticmethod
    def get(short):
        """
        Поиск ссылки по короткому идентификатору.
        """
        return URLMap.query.filter_by(short=short).first()

    @staticmethod
    def generate_short(length=LENGHT_SHORT, max_attempts=MAX_ATTEMPTS):
        """
        Генерирует уникальный короткий идентификатор.
        Ограничивает число попыток во избежание бесконечного цикла.
        """
        for _ in range(max_attempts):
            short = ''.join(random.choices(ALPHABET, k=length))
            if not URLMap.get(short):
                return short
        raise RuntimeError(GENERATE_ERROR)

    @staticmethod
    def create(original, short=None, skip_validation=False):
        """
        Создаёт и сохраняет новую запись в БД.
        """
        if not skip_validation:
            if len(original) > ORIGINAL_MAX_LENGTH:
                raise ValueError(ORIGINAL_URL_LONG)
            if short:
                if len(short) > SHORT_MAX_LENGTH or not re.match(
                    REGEXP, short
                ):
                    raise ValueError(BAD_NAME_SHORT)
                if URLMap.get(short):
                    raise ShortError(MESSAGE_FOR_SHORT)
        if not short:
            short = URLMap.generate_short()
        url_map = URLMap(original=original, short=short)
        db.session.add(url_map)
        db.session.commit()
        return url_map
