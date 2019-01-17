# -*- coding: utf-8 -*-
import unittest
import requests

class LocationTest(unittest.TestCase):
    def setUp(self):
        self.base = 'http://127.0.0.1:5000/api/v1'

    def test_get_location(self):
        url = self.base + '/location/'
        payload = {
            'name': '朝阳医院'
        }
        res = requests.get(url, params=payload)
        self.assertEqual(res.status_code, 200)
        print res.json()

