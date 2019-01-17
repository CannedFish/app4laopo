# -*- coding: utf-8 -*-
from flask_restplus import Model, fields

Location = Model('Location', {
    'name_ch': fields.String(readOnly=True\
            , description="The chinese name of hospital"),
    'lng': fields.String(readOnly=True\
            , description="The longitude of hospital"),
    'lat': fields.String(readOnly=True\
            , description="The latitude of hospital"),
    'address': fields.String(readOnly=True\
            , description="The address of hospital")
})

