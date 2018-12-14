# -*- coding: utf-8 -*-

import logging

from flask_restplus import Namespace, Resource

from .serializers import Hospital as HospitalSerializer\
        , HospitalList as HospitalListSerializer
from .models import Hospital as HospitalModel

LOG = logging.getLogger(__name__)

api = Namespace('hospital'
        , description='Hospital related operations'
        , path='/hospital')
hospital = HospitalSerializer.ins(api)
hospital_list = HospitalListSerializer.ins(api, hospital)

@api.route('/')
class HospitalList(Resource):
    @api.doc('list hospitals')
    @api.marshal_list_with(hospital)
    def get(self):
        return HospitalModel.list()

    @api.doc('create hospital')
    @api.expect(hospital_list)
    @api.marshal_with(hospital_list, code=201)
    def post(self):
        return HospitalModel.create(api.payload), 201

@api.route('/<string:hospital_id>')
@api.response(404, 'Hospital not found')
@api.param('hospital_id', 'The hospital identifier')
class Hospital(Resource):
    def get(self, hospital_id):
        res = HospitalModel.get(hospital_id)
        LOG.debug('Get a hospital: %r' % res)
        return res.to_dict() if res is not None \
                else api.abort(404, "Hospital %s dosen't exist" % hospital_id)

