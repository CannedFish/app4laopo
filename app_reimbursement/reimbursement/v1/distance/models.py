# -*- coding: utf8 -*-

import logging

from reimbursement.database import db

LOG = logging.getLogger(__name__)

class Distance(db.Model):
    src_id = db.Column(db.String(64), db.ForeignKey('hospital.id')\
            , nullable=False, primary_key=True)
    dst_id = db.Column(db.String(64), db.ForeignKey('hospital.id')\
            , nullable=False, primary_key=True)
    distance = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return '<Distance %r to %r => %d>' % \
                (src_id, dst_id, distance)

