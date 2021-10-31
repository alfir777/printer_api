from rest_framework.serializers import ModelSerializer

from .models import Check


class ChecksSerializer(ModelSerializer):
    class Meta:
        model = Check
        fields = '__all__'
