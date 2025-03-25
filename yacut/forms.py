from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, URLField
from wtforms.validators import URL, DataRequired, Length, Optional

from yacut.constants import (
    LONG_LINK, ORIGINAL_MAX_LENGTH,
    ORIGINAL_MIN_LENGTH, REQUIRED_FIELD, SHORT_LINK,
    SHORT_MAX_LENGTH, TOO_LONG_LINK, WRONG_URL
)


class YaCutForm(FlaskForm):
    """
    Форма для ссылок.
    """
    original_link = URLField(
        LONG_LINK,
        validators=[
            DataRequired(message=REQUIRED_FIELD),
            Length(ORIGINAL_MIN_LENGTH, ORIGINAL_MAX_LENGTH),
            URL(require_tld=True, message=WRONG_URL)
        ]
    )
    custom_id = StringField(
        SHORT_LINK,
        validators=[
            Length(max=SHORT_MAX_LENGTH, message=TOO_LONG_LINK),
            Optional(),
        ]
    )
    create = SubmitField('СОЗДАТЬ')