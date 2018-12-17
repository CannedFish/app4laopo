# -*- coding: utf8 -*-
from flask_restplus import Model, fields

from reimbursement.v1.hospital.serializers import Hospital

Distance = Model('Distance', {
    'src': fields.Nested(Hospital, required=True\
            , description="The source hospital unique identifier"),
    'dst': fields.Nested(Hospital, required=True\
            , description="The destination, hospital unique identifier"),
    'distance': fields.String(readOnly=True\
            , description="The distance between two hospitals")
})

