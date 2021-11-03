import json

from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from core.models import Printer, Check
from core.serializers import ChecksSerializer


class ChecksApiTestCase(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create(username='test_username')
        printer1 = Printer.objects.create(
            name='Printer 1',
            api_key='Ключ доступа к API',
            check_type='kitchen',
            point_id=1
        )
        printer2 = Printer.objects.create(
            name='Printer 2',
            api_key='Ключ доступа к API',
            check_type='client',
            point_id=2
        )
        cls.check1 = Check.objects.create(
            printer_id=printer1,
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
            printer_id=printer2,
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
        url = reverse('check-list')
        response = self.client.get(url)
        serializer_data = ChecksSerializer([self.check1, self.check2], many=True).data
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(serializer_data, response.data)

    def test_create(self):
        url = reverse('check-list')
        data = {
            "id": 3,
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
            "printer_id": 1
        }
        json_data = json.dumps(data)
        self.client.force_login(self.user)
        response = self.client.post(url, data=json_data,
                                    content_type='application/json')
        self.assertEqual(status.HTTP_201_CREATED, response.status_code)

    def test_update(self):
        url = reverse('check-detail', args=(self.check1.pk,))
        data = {
            "id": self.check1.pk,
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
            "status": "printed",
            "printer_id": 1
        }
        json_data = json.dumps(data)
        self.client.force_login(self.user)
        response = self.client.put(url, data=json_data,
                                   content_type='application/json')
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.check1.refresh_from_db()
        self.assertEqual("printed", self.check1.status)

    def test_delete(self):
        url = reverse('check-detail', args=(self.check1.pk,))
        self.client.force_login(self.user)
        response = self.client.delete(url)
        self.assertEqual(status.HTTP_204_NO_CONTENT, response.status_code)
