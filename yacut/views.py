import hashlib
import random
import re
from http import HTTPStatus

from flask import abort, flash, redirect, render_template, url_for

from yacut.constants import MESSAGE_FOR_SHORT_LINK, REGEXP, SHORT_MAX_LENGTH
from yacut.exceptions import ShortIdError
from yacut.forms import YaCutForm
from yacut.models import URLMap
from . import app, db


def get_unique_short_id(url):
    """
    Функция создания  short ссылки.
    """
    generaited_short_id = random.choices(
        hashlib.md5(url.encode()).hexdigest(), k=6
    )
    short_id = ''.join(generaited_short_id)
    while get_short_from_db(short_id) is not None:
        get_unique_short_id(url)
    return short_id


def get_short_from_db(short):
    """
    Проверяет наличие в базе данных.
    """
    return URLMap.query.filter_by(short=short).first()


def save_in_db(short_id, original):
    """
    Функция сохраняющая  ссылку и short ссылку  в базу данных.
    """
    url_map = URLMap(
        original=original,
        short=short_id,
    )
    db.session.add(url_map)
    db.session.commit()


def validate_custom_id(custom_id):
    """
    Функция валидирующая кастомуню ссылку.
    """
    return bool(
        len(custom_id) > SHORT_MAX_LENGTH or
        not re.match(REGEXP, custom_id)
    )


def creating_custom_id(custom_id, original):
    """
    Функция создает и сохраняет.
    """
    if not custom_id or custom_id == '':
        custom_id = get_unique_short_id(original)
    else:
        if validate_custom_id(custom_id):
            raise ValueError()
        if get_short_from_db(custom_id) is not None:
            raise ShortIdError()

    save_in_db(
        custom_id,
        original,
    )
    return custom_id


@app.route('/', methods=['GET', 'POST'])
def index_view():
    """
    Функция обрабатывающая запросы.
    GET запрос отображает форму на экране.
    POST запрос создает короткую ссылку.
    """
    if YaCutForm().validate_on_submit():
        try:
            custom_id = creating_custom_id(
                YaCutForm().custom_id.data,
                YaCutForm().original_link.data
            )
        except ShortIdError:
            flash(MESSAGE_FOR_SHORT_LINK, 'error')
            return render_template('yacut.html', form=YaCutForm())
        flash(url_for(
            'redirect_short_url',
            short=custom_id,
            _external=True), 'short_link'
        )
    return render_template('yacut.html', form=YaCutForm())


@app.route('/<string:short>', methods=['GET'])
def redirect_short_url(short):
    """
    Функция перенаправляет на оригинальную ссылку.
    """
    url_map = get_short_from_db(short)
    if url_map is None:
        return abort(HTTPStatus.NOT_FOUND)
    return redirect(url_map.original)