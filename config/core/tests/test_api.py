from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from core.models import Printer, Check
from core.serializers import ChecksSerializer


class ChecksApiTestCase(APITestCase):
    @classmethod
    def setUpTestData(cls):
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
