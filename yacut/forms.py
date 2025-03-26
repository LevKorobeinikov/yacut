from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, URLField
from wtforms.validators import (URL, DataRequired, Length, Optional, Regexp,
                                ValidationError)

from yacut.constants import (
    BAD_NAME_SHORT_LINK, CREATE, LONG_LINK,
    MESSAGE_FOR_SHORT_LINK, ORIGINAL_MAX_LENGTH,
    REQUIRED_FIELD, SHORT_LINK, SHORT_MAX_LENGTH,
    TOO_LONG_LINK, WRONG_URL
)
from yacut.models import REGEXP, URLMap


class YaCutForm(FlaskForm):
    """
    Форма для ссылок.
    """
    original_link = URLField(
        LONG_LINK,
        validators=[
            DataRequired(message=REQUIRED_FIELD),
            Length(max=ORIGINAL_MAX_LENGTH),
            URL(require_tld=True, message=WRONG_URL)
        ]
    )
    custom_id = StringField(
        SHORT_LINK,
        validators=[
            Length(max=SHORT_MAX_LENGTH, message=TOO_LONG_LINK),
            Optional(),
            Regexp(
                regex=REGEXP,
                message=BAD_NAME_SHORT_LINK)
        ]
    )
    create = SubmitField(CREATE)

    def validate_custom_id(self, field):
        if field.data:
            if URLMap.get_by_short_id(field.data):
                raise ValidationError(MESSAGE_FOR_SHORT_LINK)
