from datetime import datetime, timezone

from yacut import db
from yacut.constants import LOCALHOST, ORIGINAL_MAX_LENGTH, SHORT_MAX_LENGTH


class URLMap(db.Model):
    """
    Модель на ссылок.
    """
    id = db.Column(db.Integer, primary_key=True)
    original = db.Column(db.String(ORIGINAL_MAX_LENGTH), nullable=False)
    short = db.Column(db.String(SHORT_MAX_LENGTH), unique=True)
    timestamp = db.Column(
        db.DateTime, index=True,
        default=datetime.now(timezone.utc)
    )

    def to_dict(self):
        """
        Сериализатор.
        """
        return dict(
            url=self.original,
            short_link=LOCALHOST + self.short,
        )