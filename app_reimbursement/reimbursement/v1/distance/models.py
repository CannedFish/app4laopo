# -*- coding: utf-8 -*-
import logging
import uuid

from sqlalchemy.orm import aliased

from reimbursement.database import db

LOG = logging.getLogger(__name__)

def _batch_create(distances):
    ret = {'distances': []}
    for distance in distances['distances']:
        d = Distance(id=str(uuid.uuid4())\
                , src_id=distance['src_id']\
                , dst_id=distance['dst_id']\
                , distance=distance['distance'])
        db.session.add(d)
        ret['distances'].append(d)
    db.session.commit()
    return ret

def _delete_distance(hospital_id):
    distances = Distance.query.filter((Distance.src_id==hospital_id) \
            | (Distance.dst_id==hospital_id)).all()
    for d in distances:
        db.session.delete(d)
    db.session.commit()
    return distances

def _cmp(x, y):
    if x['distance'] < y['distance']:
        return -1
    elif x['distance'] > y['distance']:
        return 1
    else:
        return 0

class Distance(db.Model):
    id = db.Column(db.String(64), primary_key=True)
    src_id = db.Column(db.String(64), db.ForeignKey('hospital.id')\
            , nullable=False)
    dst_id = db.Column(db.String(64), db.ForeignKey('hospital.id')\
            , nullable=False)
    distance = db.Column(db.Integer, nullable=False)

    src_hospital = db.relationship("Hospital", foreign_keys=[src_id])
    dst_hospital = db.relationship("Hospital", foreign_keys=[dst_id])

    def __repr__(self):
        return '<Distance %r to %r => %d>' % \
                (src_id, dst_id, distance)

    @classmethod
    def list(cls, args):
        from reimbursement.v1.hospital.models import Hospital
        as1 = aliased(Hospital)
        as2 = aliased(Hospital)
        if args['src'] is not None:
            res = cls.query\
                    .join(as1, Distance.src_hospital)\
                    .join(as2, Distance.dst_hospital)\
                    .filter(as1.id==args['src'])\
                    .with_entities(as1.id, as1.name_ch, as1.name_en, as1.address, as1.lng, as1.lat\
                    , as2.id, as2.name_ch, as2.name_en, as2.address, as2.lng, as2.lat, cls.distance)
        elif args['dst'] is not None:
            res = cls.query\
                    .join(as1, Distance.src_hospital)\
                    .join(as2, Distance.dst_hospital)\
                    .filter(as2.id==args['dst'])\
                    .with_entities(as1.id, as1.name_ch, as1.name_en, as1.address, as1.lng, as1.lat\
                    , as2.id, as2.name_ch, as2.name_en, as2.address, as2.lng, as2.lat, cls.distance)
        else:
            res = cls.query\
                    .join(as1, Distance.src_hospital)\
                    .join(as2, Distance.dst_hospital)\
                    .with_entities(as1.id, as1.name_ch, as1.name_en, as1.address, as1.lng, as1.lat\
                    , as2.id, as2.name_ch, as2.name_en, as2.address, as2.lng, as2.lat, cls.distance)
        LOG.debug("query string is : %s" % res)
        ret = []
        for r in res:
            ret.append({
                'src': {
                    'id': r[0],
                    'name_ch': r[1],
                    'name_en': r[2],
                    'address': r[3],
                    'lng': r[4],
                    'lat': r[5]
                },
                'dst': {
                    'id': r[6],
                    'name_ch': r[7],
                    'name_en': r[8],
                    'address': r[9],
                    'lng': r[10],
                    'lat': r[11]
                },
                'distance': abs((r[12]/1000.0) - args['target'])
            })
        return sorted(ret, _cmp)[:args['num']]
        # return ret

    @classmethod
    def create(cls, data):
        return _batch_create(data)

    @classmethod
    def delete(cls, hospital_id):
        return _delete_distance(hospital_id)

