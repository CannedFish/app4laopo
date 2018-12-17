# -*- coding: utf-8 -*-

import logging

from flask_restplus import Namespace, Resource

from .serializers import Hospital as hospital\
        , HospitalList as hospital_list
from .models import Hospital as HospitalModel

LOG = logging.getLogger(__name__)

api = Namespace('hospital'
        , description='Hospital related operations'
        , path='/hospital')

api.models[hospital.name] = hospital
api.models[hospital_list.name] = hospital_list

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
    @api.doc('get a hospital')
    @api.marshal_with(hospital)
    def get(self, hospital_id):
        res = HospitalModel.get(hospital_id)
        LOG.debug('Get a hospital: %r' % res)
        return res.to_dict() if res is not None \
                else api.abort(404, "Hospital %s dosen't exist" % hospital_id)

    @api.doc('delete a hospital')
    @api.marshal_with(hospital)
    def delete(self, hospital_id):
        res = HospitalModel.delete(hospital_id)
        return res.to_dict() \
                if res is not None \
                else api.abort(404, "Hospital %s dosen't exist" % hospital_id)

    @api.doc('update a hospital')
    @api.expect(hospital)
    @api.marshal_with(hospital)
    def put(self, hospital_id):
        LOG.debug('Update hospital %s: %s' % (hospital_id, api.payload))
        res = HospitalModel.update(hospital_id, api.payload)
        return res.to_dict() \
                if res is not None \
                else api.abort(404, "Hospital %s dosen't exist" % hospital_id)

