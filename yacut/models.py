from datetime import datetime

from flask import url_for

from yacut import db
from random import choices
from string import ascii_letters, digits


class URLMap(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    original = db.Column(db.Text, nullable=False, index=True)
    short = db.Column(db.String(16), unique=True, nullable=False)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)

    def to_dict(self):
        return dict(
            url=self.original,
            short_link=url_for(
                'short_link_view',
                short=self.short,
                _external=True
            )
        )

    def from_dict(self, data):
        setattr(self, 'original', data['url'])
        setattr(self, 'short', data['custom_id'])

    def get_unique_short_id(list=ascii_letters + digits, k=6):
        while True:
            short_id = ''.join(choices(list, k=k))
            if not URLMap.query.filter_by(short=short_id).first():
                return short_id
