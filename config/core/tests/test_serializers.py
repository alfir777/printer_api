from django.contrib.auth.models import User
from django.test import TestCase

from core.models import Printer, Check
from core.serializers import ChecksSerializer


class ChecksSerializerTestCase(TestCase):
    printer1 = None
    printer2 = None

    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create(username='test_username')
        cls.printer1 = Printer.objects.create(
            name='Printer 1',
            api_key='Ключ доступа к API',
            check_type='kitchen',
            point_id=1
        )
        cls.printer2 = Printer.objects.create(
            name='Printer 2',
            api_key='Ключ доступа к API',
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

    def test_ok(self):
        self.client.force_login(self.user)
        serializer_data = ChecksSerializer([self.check1, self.check2], many=True).data
        expected_data = [
            {
                "id": self.check1.pk,
                "type": "kitchen",
                "order": {
                    "id": 123456,
                    "items": [
                        {
                            "name": "Вкусная пицца",
                            "quantity": 2,
                            "unit_price": 250
                        },
                        {
                            "name": "Не менее вкусные роллы",
                            "quantity": 1,
                            "unit_price": 280
                        }
                    ],
                    "price": 780,
                    "client": {
                        "name": "Иван",
                        "phone": 9173332222
                    },
                    "address": "г. Уфа, ул. Ленина, д. 42",
                    "point_id": 1
                },
                "status": "new",
                "pdf_file": None,
                "printer_id": self.printer1.pk
            },
            {
                "id": self.check2.pk,
                "type": "client",
                "order": {
                    "id": 123456,
                    "items": [
                        {
                            "name": "Вкусная пицца",
                            "quantity": 2,
                            "unit_price": 250
                        },
                        {
                            "name": "Не менее вкусные роллы",
                            "quantity": 1,
                            "unit_price": 280
                        }
                    ],
                    "price": 780,
                    "client": {
                        "name": "Иван",
                        "phone": 9173332222
                    },
                    "address": "г. Уфа, ул. Ленина, д. 42",
                    "point_id": 1
                },
                "status": "new",
                "pdf_file": None,
                "printer_id": self.printer2.pk
            },
        ]
        self.assertEqual(expected_data, serializer_data)
