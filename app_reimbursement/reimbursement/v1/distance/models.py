# -*- coding: utf-8 -*-
import logging

from sqlalchemy.orm import aliased

from reimbursement.database import db

LOG = logging.getLogger(__name__)

def _batch_create(distances):
    ret = {'distances': []}
    for distance in distances['distances']:
        d = Distance(src_id=distance['src_id']\
                , dst_id=distance['dst_id']\
                , distance=distance['distance'])
        db.session.add(d)
        ret['distances'].append(d)
    db.session.commit()
    return ret

class Distance(db.Model):
    src_id = db.Column(db.String(64), db.ForeignKey('hospital.id')\
            , nullable=False, primary_key=True)
    dst_id = db.Column(db.String(64), db.ForeignKey('hospital.id')\
            , nullable=False, primary_key=True)
    distance = db.Column(db.Integer, nullable=False)

    src_hospital = db.relationship("Hospital", foreign_keys=[src_id])
    dst_hospital = db.relationship("Hospital", foreign_keys=[dst_id])

    def __repr__(self):
        return '<Distance %r to %r => %d>' % \
                (src_id, dst_id, distance)

    @classmethod
    def list(cls, args):
        if args['src'] is not None:
            return cls.query.join(Distance.src_hospital, Distance.src_id==args['src']).all()
        else:
            from reimbursement.v1.hospital.models import Hospital
            as1 = aliased(Hospital)
            as2 = aliased(Hospital)
            return cls.query\
                    .join(as1, Distance.src_hospital)\
                    .join(as2, Distance.dst_hospital)\
                    .filter(Distance.src_id==as1.id)\
                    .filter(Distance.dst_id==as2.id)\
                    .all()

    @classmethod
    def create(cls, data):
        return _batch_create(data)

