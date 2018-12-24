# -*- coding: utf-8 -*-
import unittest
import random
import uuid
import requests
import json

from .utils import cal_distance\
        , trans_new_hospital_to_distance

class Pos(object):
    def __init__(self, lng, lat):
        self.id = str(uuid.uuid4())
        self.lng = lng
        self.lat = lat

class UtilsTest(unittest.TestCase):
    def test_cal_distance(self):
        src = Pos(40.45, 116.34)
        dst = [Pos(round(random.uniform(40, 42), 2), \
                round(random.uniform(116, 118), 2), \
                ) for _ in range(3)]
        res = cal_distance(src, dst)
        self.assertEqual(res['status'], 0)
        self.assertEqual(len(res['result']), 3)
        print res

    def test_trans_new_hospital_to_distance(self):
        res = trans_new_hospital_to_distance([Pos(round(random.uniform(40, 42), 2), \
                round(random.uniform(116, 118), 2), \
                ) for _ in range(3)])
        self.assertEqual(len(old), 5)

class DistanceTest(unittest.TestCase):
    def setUp(self):
        self.base = 'http://127.0.0.1:5000/api/v1'
        self._create_hospital()

    def tearDown(self):
        self._remove_hospitals()

    def _create_hospital(self):
        url = self.base + '/hospital/'
        data = {
            "hospitals": [
                {
                    'name_ch': 'A医院',
                    'name_en': 'A hospital',
                    'address': 'Some where A',
                    'lng': 40.45,
                    'lat': 116.34
                },
                {
                    'name_ch': 'B医院',
                    'name_en': 'B hospital',
                    'address': 'Some where B',
                    'lng': 40.35,
                    'lat': 116.46
                }
            ]
        }
        headers = {
            'Content-Type': 'application/json'
        }
        res = requests.post(url, data=json.dumps(data), headers=headers)
        self.assertEqual(res.status_code, 201)
        self._hospitals = res.json()
        return self._hospitals

    def _remove_hospitals(self):
        for h in self._hospitals['hospitals']:
            url = self.base + '/hospital/' + h['id']
            res = requests.delete(url)
            self.assertEqual(res.status_code, 200)
        return res.json()

    def _test_list_all(self):
        url = self.base + '/distance/'
        payload = {
            'num': 10,
            'target': 20
        }
        res = requests.get(url, params=payload)
        self.assertEqual(res.status_code, 200)
        print res.json()

    def _test_list_src(self):
        url = self.base + '/distance/'
        payload = {
            'num': 10,
            'target': 20,
            'src': self._hospitals['hospitals'][0]['id']
        }
        res = requests.get(url, params=payload)
        self.assertEqual(res.status_code, 200)
        print res.json()

    def _test_list_dst(self):
        url = self.base + '/distance/'
        payload = {
            'num': 10,
            'target': 20,
            'dst': self._hospitals['hospitals'][0]['id']
        }
        res = requests.get(url, params=payload)
        self.assertEqual(res.status_code, 200)
        print res.json()

    def test_list(self):
        self._test_list_all()
        self._test_list_src()
        self._test_list_dst()

