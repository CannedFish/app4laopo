# -*- coding: utf-8 -*-

from flask_restplus import fields

class Hospital(object):
    @classmethod
    def ins(cls, api):
        return api.model('Hospital', {
            'id': fields.String(readOnly=True, description="The hospital unique identifier"),
            'name_ch': fields.String(required=True, description="The chinses name of hospital"),
            'name_en': fields.String(required=False, description="The english name of hospital"),
            'address': fields.String(required=True, description="The address of hospital"),
        })

class HospitalList(object):
    @classmethod
    def ins(cls, api, hospital):
        return api.model('HospitalList', {
            'hospitals': fields.List(fields.Nested(hospital))
        })

