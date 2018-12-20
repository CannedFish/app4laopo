# -*- coding: utf8 -*-
import logging

from flask_restplus import Namespace, Resource\
        , reqparse

from .serializers import Distance as distance
from .models import Distance as DistanceModel

LOG = logging.getLogger(__name__)

api = Namespace('disks'
        , description='Disks related operations'
        , path='/distance')

api.models[distance.name] = distance

@api.route('/')
class DistanceList(Resource):
    distance_list_parser = reqparse.RequestParser()
    distance_list_parser.add_argument('num', type=int\
            , help='Number to be returned', default=20)
    distance_list_parser.add_argument('target', type=int\
            , help='Target distance to query', default=-1)
    distance_list_parser.add_argument('src'\
            , help='Source hospital', default=None)
    distance_list_parser.add_argument('dst'\
            , help='Destination hospital', default=None)

    @api.doc('list distances')
    @api.expect(distance_list_parser)
    @api.marshal_list_with(distance)
    def get(self):
        args = self.distance_list_parser.parse_args()
        LOG.debug("Arguments: %s" % args)
        return DistanceModel.list(args)

