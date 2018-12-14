# -*- coding: utf8 -*-

import logging
import uuid
from datetime import datetime

from reimbursement.database import db

LOG = logging.getLogger(__name__)

def _batch_create(hospitals):
    ret = {'hospitals': []}
    for hospital in hospitals['hospitals']:
        h = Hospital(id=str(uuid.uuid4())
            , name_ch=hospital['name_ch']
            , name_en=hospital['name_en']
            , address=hospital['address'])
        db.session.add(h)
        ret['hospitals'].append(h)
    db.session.commit()
    return ret

class Hospital(db.Model):
    id = db.Column(db.String(64), primary_key=True)
    name_ch = db.Column(db.String(256), unique=True, nullable=False)
    name_en = db.Column(db.String(256), unique=True, nullable=True)
    address = db.Column(db.String(256), unique=True, nullable=False)
    pub_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    def __repr__(self):
        return '<Hospital %r, %r(%r), %r, %r>' % \
                (self.id, self.name_ch, self.name_en, self.address, self.pub_date)

    @classmethod
    def list(cls):
        return cls.query.all()

    @classmethod
    def get(cls, hospital_id):
        return cls.query.filter_by(id=hospital_id).first()

    @classmethod
    def create(cls, hospitals):
        return _batch_create(hospitals)

    def to_dict(self):
        return {
            'id': self.id,
            'name_ch': self.name_ch,
            'name_en': self.name_en,
            'address': self.address,
            'pub_date': str(self.pub_date)
        }

