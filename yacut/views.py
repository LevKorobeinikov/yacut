from http import HTTPStatus

from flask import abort, flash, redirect, render_template

from yacut.constants import BAD_NAME_SHORT, GENERATE_ERROR, MESSAGE_FOR_SHORT
from yacut.exceptions import ShortError
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
    short_url = None
    if form.validate_on_submit():
        try:
            url_map = URLMap.create(
                form.original_link.data,
                form.custom_id.data
            )
            short_url = url_map.get_short_url()
        except ValueError:
            flash(BAD_NAME_SHORT, 'error')
        except ShortError:
            flash(MESSAGE_FOR_SHORT, 'error')
        except RuntimeError:
            flash(GENERATE_ERROR)
    return render_template(
        'index.html', form=form, short_url=short_url
    )


@app.route('/<string:short>', methods=['GET'])
def redirect_short(short):
    """
    Перенаправляет пользователя на оригинальную ссылку.
    """
    url_map = URLMap.get(short)
    if not url_map:
        abort(HTTPStatus.NOT_FOUND)
    return redirect(url_map.original)
