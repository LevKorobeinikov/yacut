from http import HTTPStatus

from flask import jsonify, request

from yacut.constants import (
    BAD_NAME_SHORT_LINK, ID_NOT_FOUND,
    MESSAGE_FOR_SHORT_LINK, MISSING_REQUEST, URL_MISSING
)
from yacut.error_handlers import InvalidAPIUsage
from yacut.exceptions import ShortIdError
from yacut.models import URLMap
from yacut.views import creating_custom_id, get_short_from_db

from . import app


@app.route('/api/id/<short_id>/', methods=['GET'])
def get_original_url(short_id):
    """
    GET-запрос на получение оригинальной ссылки
    по указанному короткому идентификатору.
    """
    url_map = get_short_from_db(short_id)
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
    try:
        custom_id = creating_custom_id(data.get('custom_id'), original)
    except ValueError:
        raise InvalidAPIUsage(BAD_NAME_SHORT_LINK)
    except ShortIdError:
        raise InvalidAPIUsage(MESSAGE_FOR_SHORT_LINK)
    return jsonify(
        URLMap(
            original=original,
            short=custom_id
        ).to_dict()
    ), HTTPStatus.CREATED