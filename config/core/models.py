from django.db import models


class Printer(models.Model):
    name = models.CharField(max_length=150, verbose_name='Название принтера')
    api_key = models.CharField(max_length=500, verbose_name='Ключ доступа к API')
    check_type_choices = (
        ('kitchen', 'kitchen'),
        ('client', 'client'),
    )
    check_type = models.CharField(max_length=150, choices=check_type_choices, verbose_name='Тип чека')
    point_id = models.IntegerField(verbose_name='точка')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Принтер'
        verbose_name_plural = 'Принтеры'


class Check(models.Model):
    printer_id = models.ForeignKey(Printer, on_delete=models.PROTECT, verbose_name='Принтер')
    type_choices = (
        ('kitchen', 'kitchen'),
        ('client', 'client'),
    )
    type = models.CharField(max_length=150, choices=type_choices, verbose_name='Тип чека')
    order = models.JSONField(verbose_name='информация о заказе')
    status_choices = (
        ('new', 'new'),
        ('rendered', 'rendered'),
        ('printed', 'printed'),
    )
    status = models.CharField(max_length=150, choices=status_choices, verbose_name='статус чека')
    pdf_file = models.FileField(upload_to='pdf', blank=True, verbose_name='ссылка на созданный PDF-файл', default=None)

    def __str__(self):
        return f'Чек № {self.pk}'

    class Meta:
        verbose_name = 'Чек'
        verbose_name_plural = 'Чеки'
