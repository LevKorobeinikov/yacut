import string
import re

ALPHABET = string.ascii_letters + string.digits
BAD_NAME_SHORT = 'Указано недопустимое имя для короткой ссылки'
CREATE = 'СОЗДАТЬ'
MAX_ATTEMPTS = 10
GENERATE_ERROR = (
    f'Не удалось сгенерировать идентификатор после {MAX_ATTEMPTS} попыток '
)
ID_NOT_FOUND = 'Указанный id не найден'
LENGHT_SHORT = 6
LONG_LINK = 'Введите длинную ссылку'
MESSAGE_FOR_SHORT = 'Предложенный вариант короткой ссылки уже существует.'
MISSING_REQUEST = 'Отсутствует тело запроса'
ORIGINAL_MAX_LENGTH = 500
ORIGINAL_URL_LONG = 'Оригинальная ссылка сликшом длинная.'
REDIRECT_SHORT = 'redirect_short'
REGEXP = f'^[{re.escape(ALPHABET)}]+$'
REQUIRED_FIELD = 'Обязательное поле'
SHORT_LINK = 'Введите вашу короткую ссылку'
SHORT_MAX_LENGTH = 16
TOO_LONG_LINK = f'Длина больше {SHORT_MAX_LENGTH} символов'
URL_MISSING = '"url" является обязательным полем!'
WRONG_URL = 'Провертье вводимый адрес'
