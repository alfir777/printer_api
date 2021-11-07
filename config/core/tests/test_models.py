from django.test import TestCase

from core.models import Printer, Check


class PrinterModelTestCase(TestCase):
    printer1 = None

    @classmethod
    def setUpTestData(cls):
        cls.printer1 = Printer.objects.create(
            name='Printer 1',
            api_key='12345',
            check_type='kitchen',
            point_id=1
        )

    def test_get(self):
        self.assertEqual(str(self.printer1), 'Printer 1')


class CheckModelTestCase(TestCase):
    check1 = None

    @classmethod
    def setUpTestData(cls):
        cls.printer1 = Printer.objects.create(
            name='Printer 1',
            api_key='12345',
            check_type='kitchen',
            point_id=1
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

    def test_get(self):
        self.assertEqual(str(self.check1), f'Чек № {self.check1.pk}')
