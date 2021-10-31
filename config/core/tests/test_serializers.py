from django.test import TestCase

from core.models import Printer, Check
from core.serializers import ChecksSerializer


class ChecksSerializerTestCase(TestCase):
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

    def test_ok(self):
        serializer_data = ChecksSerializer([self.check1, self.check2], many=True).data
        expected_data = [
            {
                "id": 3,
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
                "printer_id": 3
            },
            {
                "id": 4,
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
                "printer_id": 4
            },
        ]
        self.assertEqual(expected_data, serializer_data)
