import json
import os

from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.test import APITestCase

from config.settings import BASE_DIR
from core.models import Printer, Check
from core.serializers import ChecksSerializer


class ErpApiTestCase(APITestCase):

    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create(username='test_username')

        cls.printer1 = Printer.objects.create(
            name='Printer 1',
            api_key='12345',
            check_type='kitchen',
            point_id=1
        )

    def test_create(self):
        self.client.force_login(self.user)
        data = {
            "type": "client",
            "order": {"id": 123457,
                      "items": [
                          {"name": "Пицца", "quantity": 1, "unit_price": 250},
                          {"name": "Филадельфия", "quantity": 1, "unit_price": 400}
                      ],
                      "price": 650,
                      "client": {"name": "Петр", "phone": 9173332242},
                      "address": "г. Уфа, ул. Московская, д. 102",
                      "point_id": 1},
            "status": "new",
            "printer_id": self.printer1.pk
        }
        json_data = json.dumps(data)
        response = self.client.post('/create_checks/', data=json_data,
                                    content_type='application/json')
        self.assertEqual(status.HTTP_201_CREATED, response.status_code)

    def test_code_400(self):
        self.client.force_login(self.user)
        data = {
            "type": "client",
            "order": {"id": 123457,
                      "items": [
                          {"name": "Пицца", "quantity": 1, "unit_price": 250},
                          {"name": "Филадельфия", "quantity": 1, "unit_price": 400}
                      ],
                      "price": 650,
                      "client": {"name": "Петр", "phone": 9173332242},
                      "address": "г. Уфа, ул. Московская, д. 102",
                      "point_id": 1},
            "status": "new",
            "printer_id": 9173332242
        }
        json_data = json.dumps(data)
        response = self.client.post('/create_checks/', data=json_data,
                                    content_type='application/json')
        self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)

    def test_code_403(self):
        data = {
            "type": "client",
            "order": {"id": 123457,
                      "items": [
                          {"name": "Пицца", "quantity": 1, "unit_price": 250},
                          {"name": "Филадельфия", "quantity": 1, "unit_price": 400}
                      ],
                      "price": 650,
                      "client": {"name": "Петр", "phone": 9173332242},
                      "address": "г. Уфа, ул. Московская, д. 102",
                      "point_id": 1},
            "status": "new",
            "printer_id": 9173332242
        }
        json_data = json.dumps(data)
        response = self.client.post('/create_checks/', data=json_data,
                                    content_type='application/json')
        self.assertEqual(status.HTTP_403_FORBIDDEN, response.status_code)


class AppApiTestCase(APITestCase):
    printer1 = None
    printer2 = None

    @classmethod
    def setUpTestData(cls):
        cls.printer1 = Printer.objects.create(
            name='Printer 1',
            api_key='12345',
            check_type='kitchen',
            point_id=1
        )
        cls.printer2 = Printer.objects.create(
            name='Printer 2',
            api_key='123456789',
            check_type='client',
            point_id=2
        )
        cls.check1 = Check.objects.create(
            printer_id=cls.printer1,
            type='kitchen',
            order={"id": 123456,
                   "items": [{"name": "Вкусная пицца", "quantity": 2, "unit_price": 250},
                             {"name": "Не менее вкусные роллы", "quantity": 1, "unit_price": 280}],
                   "price": 780,
                   "client": {"name": "Иван", "phone": 9173332222},
                   "address": "г. Уфа, ул. Ленина, д. 42",
                   "point_id": 1},
            status='new',
            pdf_file='',
        )
        cls.check2 = Check.objects.create(
            printer_id=cls.printer2,
            type='client',
            order={"id": 123456,
                   "items": [{"name": "Вкусная пицца", "quantity": 2, "unit_price": 250},
                             {"name": "Не менее вкусные роллы", "quantity": 1, "unit_price": 280}],
                   "price": 780,
                   "client": {"name": "Иван", "phone": 9173332222},
                   "address": "г. Уфа, ул. Ленина, д. 42",
                   "point_id": 1},
            status='new',
            pdf_file='',
        )

    def test_get(self):
        response = self.client.get(f'/new_checks/{self.printer1.api_key}/', follow=True)
        serializer_data = ChecksSerializer([self.check1, self.check2], many=True).data
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(serializer_data, response.data)

    def test_api_key(self):
        response = self.client.get(f'/new_checks/9173332242/', follow=True)
        self.assertEqual(status.HTTP_401_UNAUTHORIZED, response.status_code)


class AppPdfApiTestCase(APITestCase):
    check2 = None
    check1 = None
    printer1 = None
    printer2 = None

    @classmethod
    def setUpTestData(cls):
        cls.printer1 = Printer.objects.create(
            name='Printer 1',
            api_key='12345',
            check_type='kitchen',
            point_id=1
        )
        cls.printer2 = Printer.objects.create(
            name='Printer 2',
            api_key='123456789',
            check_type='client',
            point_id=2
        )
        cls.check1 = Check.objects.create(
            printer_id=cls.printer1,
            type='kitchen',
            order={"id": 123456,
                   "items": [{"name": "Вкусная пицца", "quantity": 2, "unit_price": 250},
                             {"name": "Не менее вкусные роллы", "quantity": 1, "unit_price": 280}],
                   "price": 780,
                   "client": {"name": "Иван", "phone": 9173332222},
                   "address": "г. Уфа, ул. Ленина, д. 42",
                   "point_id": 1},
            status='new',
            pdf_file=os.path.join(BASE_DIR, 'media/test/123456_kitchen.pdf'),
        )
        cls.check2 = Check.objects.create(
            printer_id=cls.printer2,
            type='client',
            order={"id": 123456,
                   "items": [{"name": "Вкусная пицца", "quantity": 2, "unit_price": 250},
                             {"name": "Не менее вкусные роллы", "quantity": 1, "unit_price": 280}],
                   "price": 780,
                   "client": {"name": "Иван", "phone": 9173332222},
                   "address": "г. Уфа, ул. Ленина, д. 42",
                   "point_id": 1},
            status='new',
            pdf_file='',
        )

    def test_get(self):
        response = self.client.get(f'/check/{self.check1.pk}/{self.printer1.api_key}/')
        self.assertEqual(status.HTTP_200_OK, response.status_code)

    def test_api_key(self):
        response = self.client.get(f'/check/{self.check1.pk}/9173332242/')
        self.assertEqual(status.HTTP_401_UNAUTHORIZED, response.status_code)

    def test_get_check1_pk(self):
        response = self.client.get(f'/check/9173332242/{self.printer1.api_key}/')
        self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)
