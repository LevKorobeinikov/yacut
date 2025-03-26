from http import HTTPStatus

from flask import abort, flash, redirect, render_template

from yacut.constants import MESSAGE_FOR_SHORT_LINK
from yacut.exceptions import ShortIdError
from yacut.forms import YaCutForm
from yacut.models import URLMap

from . import app


@app.route('/', methods=['GET', 'POST'])
def index_view():
    """
    Обработчик главной страницы.
    - GET: отображает форму.
    - POST: создаёт короткую ссылку.
    """
    form = YaCutForm()
    short = None
    if form.validate_on_submit():
        try:
            url_map = URLMap.create(
                form.original_link.data,
                form.custom_id.data
            )
            short = url_map.get_short_url()
        except ShortIdError:
            flash(MESSAGE_FOR_SHORT_LINK, 'error')
            return render_template('index.html', form=YaCutForm())
    return render_template('index.html', form=form, short=short)


@app.route('/<string:short>', methods=['GET'])
def redirect_short_url(short):
    """
    Перенаправляет пользователя на оригинальную ссылку.
    """
    url_map = URLMap.get_by_short_id(short)
    if not url_map:
        abort(HTTPStatus.NOT_FOUND)
    return redirect(url_map.original)
