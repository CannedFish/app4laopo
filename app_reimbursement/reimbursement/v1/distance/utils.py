# -*- coding: utf8 -*-

import logging
import requests

from reimbursement.settings import KEY

LOG = logging.getLogger(__name__)

def cal_distance(src, dsts):
    """
    :param src object<HospitalModel>: origin of hospital
    :param dsts array<HospitalModel>: destinations of hospital
    """
    url = 'http://api.map.baidu.com/routematrix/v2/driving'
    payload = {
        'output': 'json',
        'origins': '%f,%f' % (src.lng, src.lat),
        'destinations': '|'.join(['%f,%f' % (dst.lng, dst.lat) for dst in dsts]),
        'ak': KEY
    }
    res = requests.get(url, params=payload)
    LOG.debug("Calculate distances request to %s" % res.url)

