from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, URLField
from wtforms.validators import URL, DataRequired, Length, Optional, Regexp, ValidationError

from .models import URLMap
from .constants import MAX_CUSTOM_SIZE, MAX_LINK_SIZE, LINK


class UrlForm(FlaskForm):
    original_link = URLField(
        'Введите ссылку для укорачивания',
        validators=[
            DataRequired(message='Обязательное поле'),
            Length(max=MAX_LINK_SIZE),
            URL(require_tld=True, message='Некорректный URL')
        ]
    )
    custom_id = StringField(
        'Ваша короткая ссылка',
        validators=[
            Length(max=MAX_CUSTOM_SIZE),
            Optional(),
            Regexp(regex=LINK,
                   message='Только лат.буквы и цифры 0-9 ')
        ]
    )
    submit = SubmitField('Сгенерировать')

    def validate_custom_id(self, field):
        if field.data and URLMap.query.filter_by(short=field.data).first():
            raise ValidationError('Предложенный вариант короткой ссылки уже существует.')
