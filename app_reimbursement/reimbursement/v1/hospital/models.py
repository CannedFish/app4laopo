# -*- coding: utf8 -*-
import logging
import uuid
from datetime import datetime

from reimbursement.database import db
from reimbursement.v1.distance.utils import trans_new_hospital_to_distance

LOG = logging.getLogger(__name__)

def _batch_create(hospitals):
    old = Hospital.list()
    ret = {'hospitals': []}
    for hospital in hospitals['hospitals']:
        h = Hospital(id=str(uuid.uuid4())
            , name_ch=hospital['name_ch']
            , name_en=hospital['name_en']
            , address=hospital['address']
            , lng=hospital['lng']
            , lat=hospital['lat'])
        db.session.add(h)
        ret['hospitals'].append(h)
    db.session.commit()
    trans_new_hospital_to_distance(ret['hospitals'], old)
    return ret

def _delete(hospital_id):
    hospital = Hospital.get(hospital_id)
    if hospital is not None:
        db.session.delete(hospital)
        db.session.commit()
    return hospital

def _update(hospital_id, data):
    hospital = Hospital.get(hospital_id)
    if hospital is not None:
        for key in [_ for _ in data if _ not in ['id', 'pub_date']]:
            setattr(hospital, key, data[key])
        db.session.commit()
    return hospital

class Hospital(db.Model):
    id = db.Column(db.String(64), primary_key=True)
    name_ch = db.Column(db.String(256), unique=True, nullable=False)
    name_en = db.Column(db.String(256), unique=True, nullable=True)
    address = db.Column(db.String(256), unique=True, nullable=False)
    pub_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    lng = db.Column(db.Float, nullable=False)
    lat = db.Column(db.Float, nullable=False)

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

    @classmethod
    def delete(cls, hospital_id):
        return _delete(hospital_id)

    @classmethod
    def update(cls, hospital_id, data):
        return _update(hospital_id, data)

    def to_dict(self):
        return {
            'id': self.id,
            'name_ch': self.name_ch,
            'name_en': self.name_en,
            'address': self.address,
            'pub_date': str(self.pub_date),
            'lng': self.lng,
            'lat': self.lat
        }

