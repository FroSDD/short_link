from http import HTTPStatus
from flask import jsonify, request
from re import match

from . import app, db
from .constants import API_LINK_LONG, API_LINK_SHORT
from .error_handlers import InvalidAPIUsage
from .models import URLMap


@app.route('/api/id/', methods=['POST'])
def add_url():
    data = request.get_json()
    if not data:
        raise InvalidAPIUsage('Отсутствует тело запроса')
    if 'url' not in data:
        raise InvalidAPIUsage('"url" является обязательным полем!')
    if not match(
            API_LINK_LONG, data['url']):
        raise InvalidAPIUsage('Введен некорректный URL')
    if not data.get('custom_id'):
        data['custom_id'] = URLMap.get_unique_short_id()
    if not match(API_LINK_SHORT, data['custom_id']):
        raise InvalidAPIUsage(
            'Указано недопустимое имя для короткой ссылки')
    if URLMap.query.filter_by(short=data['custom_id']).first():
        raise InvalidAPIUsage('Предложенный вариант короткой ссылки уже существует.')
    url_map = URLMap()
    url_map.from_dict(data)
    db.session.add(url_map)
    db.session.commit()
    return jsonify(url_map.to_dict()), HTTPStatus.CREATED


@app.route('/api/id/<string:short_id>/')
def get_short_url(short_id):
    url_map = URLMap.query.filter_by(short=short_id).first()
    if not url_map:
        raise InvalidAPIUsage(
            'Указанный id не найден', HTTPStatus.NOT_FOUND
        )
    return jsonify({'url': url_map.original})
