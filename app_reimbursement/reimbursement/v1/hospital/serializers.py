# -*- coding: utf-8 -*-

from flask_restplus import Model, fields

Hospital = Model('Hospital', {
    'id': fields.String(readOnly=True, description="The hospital unique identifier"),
    'name_ch': fields.String(required=True, description="The chinses name of hospital"),
    'name_en': fields.String(required=False, description="The english name of hospital"),
    'address': fields.String(required=True, description="The address of hospital"),
    'lng': fields.Float(required=True, description="The longitude of hospital"),
    'lat': fields.Float(required=True, description="The latitude of hospital"),
})

HospitalList = Model('HospitalList', {
    'hospitals': fields.List(fields.Nested(Hospital))
})

