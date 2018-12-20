# -*- coding: utf8 -*-

import logging

from reimbursement.database import db

LOG = logging.getLogger(__name__)

def _create_distance(data):
    pass

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
        return cls.query.all()

    @classmethod
    def create(cls, data):
        return _create_distance(data)

