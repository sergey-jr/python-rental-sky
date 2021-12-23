import json as json_lib
import os
from unittest.mock import patch

from django.test import TestCase, Client
# Create your tests here.
from requests import HTTPError
from rest_framework import status

from api.utils import get_order, make_order, extract_ski_data


class MockResponse:

    def __init__(self, file_name):
        assert os.path.exists(file_name)
        self.status_code = 200
        self.file_name = file_name

    def json(self):
        return json_lib.load(open(self.file_name))

    def raise_for_status(self):
        pass


class NoneMockResponse:
    def __init__(self):
        self.status_code = 200

    def json(self):
        return None

    def raise_for_status(self):
        pass


class TestExternalAPI(TestCase):
    def setUp(self):
        self.client = Client()

    @patch("requests.get", return_value=MockResponse('./fixtures/get_order.json'))
    def test_get_order(self, mocked):
        self.assertEqual(
            get_order(number='AAAAAA', passenger_id='ivanov'),
            json_lib.load(open('./fixtures/get_order.json'))
        )

    def test_make_order(self):
        with patch("requests.get", return_value=MockResponse('./fixtures/get_order.json')), \
                patch("requests.put", return_value=NoneMockResponse()):
            order = get_order(number='AAAAAA', passenger_id='ivanov')
            ski_data = extract_ski_data(order)
            self.assertEqual(make_order(ski_data), None)

    def test_make_order_fail(self):
        with patch("requests.get", return_value=MockResponse('./fixtures/get_order.json')):
            order = get_order(number='AAAAAA', passenger_id='ivanov')
            ski_data = extract_ski_data(order)
            with self.assertRaises((HTTPError, Exception)):
                self.assertEqual(make_order(ski_data), None)

    def test_ski_rent_initial_fail(self):
        response = self.client.get('/api/')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_get_order_fail(self):
        response = self.client.get('/api/', data={'id': 'AAAAAA', 'last_name': 'ivanov'})
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
