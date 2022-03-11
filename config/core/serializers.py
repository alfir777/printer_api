from abc import abstractmethod

from rest_framework import serializers

from .models import Check, Printer


class ChecksSerializer(serializers.ModelSerializer):
    class Meta:
        model = Check
        fields = ('id',)


class CreateChecksSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    price = serializers.IntegerField()
    items = serializers.JSONField()
    address = serializers.CharField()
    client = serializers.JSONField()
    point_id = serializers.IntegerField()

    @abstractmethod
    def save(self):
        checks = Check.objects.filter(order=self.validated_data)
        if len(checks) > 0:
            raise ValueError
        printers = Printer.objects.filter(point_id=self.validated_data['point_id'])
        if len(printers) == 0:
            raise ValueError
        else:
            for printer in printers:
                Check(printer_id=printer,
                      type=printer.check_type,
                      order=self.validated_data,
                      status='new',
                      ).save()
