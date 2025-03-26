from http import HTTPStatus

from flask import jsonify, request

from yacut.constants import (
    BAD_NAME_SHORT_LINK, ID_NOT_FOUND,
    MESSAGE_FOR_SHORT_LINK, MISSING_REQUEST,
    URL_MISSING
)
from yacut.error_handlers import InvalidAPIUsage
from yacut.exceptions import ShortIdError
from yacut.models import URLMap

from . import app


@app.route('/api/id/<short>/', methods=['GET'])
def get_original_url(short):
    """
    GET-запрос на получение оригинальной ссылки
    по указанному короткому идентификатору.
    """
    url_map = URLMap.get_by_short_id(short)
    if url_map is None:
        raise InvalidAPIUsage(
            ID_NOT_FOUND,
            HTTPStatus.NOT_FOUND
        )
    return jsonify(url=url_map.original), HTTPStatus.OK


@app.route('/api/id/', methods=['POST'])
def add_url():
    """
    POST-запрос на создание новой короткой ссылки.
    """
    if not request.data:
        raise InvalidAPIUsage(MISSING_REQUEST)
    data = request.get_json()
    if not data.get('url'):
        raise InvalidAPIUsage(URL_MISSING)
    original = data.get('url')
    short = data.get('custom_id')
    try:
        url_map = URLMap.create(original, short)
    except ValueError:
        raise InvalidAPIUsage(BAD_NAME_SHORT_LINK)
    except ShortIdError:
        raise InvalidAPIUsage(MESSAGE_FOR_SHORT_LINK)
    return jsonify(url_map.to_dict()), HTTPStatus.CREATED
