from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, URLField
from wtforms.validators import URL, DataRequired, Length, Optional, Regexp, ValidationError

from .models import URLMap


class UrlForm(FlaskForm):
    original_link = URLField(
        'Введите ссылку для укорачивания',
        validators=[
            DataRequired(message='Обязательное поле'),
            Length(1, 256),
            URL(require_tld=True, message='Некорректный URL')
        ]
    )
    custom_id = StringField(
        'Ваша короткая ссылка',
        validators=[
            Length(1, 16),
            Optional(),
            Regexp(r'^[A-Za-z0-9]+$',
                   message='Только лат.буквы и цифры 0-9 ')
        ]
    )
    submit = SubmitField('Сгенерировать')

    def validate_custom_id(self, field):
        if field.data and URLMap.query.filter_by(short=field.data).first():
            raise ValidationError(f'Имя {field.data} уже занято.')
