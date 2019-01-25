# -*- coding: utf-8 -*-
from flask_restplus import Namespace, Resource\
        , reqparse
from flask import abort, current_app

from .serializers import Location as location
from reimbursement.v1.distance.utils import location_search

api = Namespace('location'
        , description='Locations related operations'
        , path='/location')
api.models[location.name] = location

@api.route('/')
class Location(Resource):
    location_parser = reqparse.RequestParser()
    location_parser.add_argument('name', required=True\
            , help='Location name to search')

    @api.doc('get location details')
    @api.expect(location_parser)
    @api.marshal_list_with(location)
    def get(self):
        args = self.location_parser.parse_args()
        current_app.logger.debug("Arguments: %s" % args)
        ret = location_search(args['name'])
        if ret['status'] == 0:
            return [{\
                'name_ch': r['name'],\
                'lng': r['location']['lng'],\
                'lat': r['location']['lat'],\
                'address': r['address']\
            } for r in ret['results']]
        else:
            current_app.logger.error("Search failed: %d, %s" % (ret['status'], ret['message']))
            abort(400, ret['message'])

