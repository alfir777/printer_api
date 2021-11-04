from rest_framework import serializers

from .models import Check


class ChecksSerializer(serializers.ModelSerializer):
    class Meta:
        model = Check
        fields = '__all__'
