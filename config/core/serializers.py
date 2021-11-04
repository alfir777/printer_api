from rest_framework import serializers

from .models import Check


class ChecksSerializer(serializers.ModelSerializer):
    class Meta:
        model = Check
        fields = '__all__'


class CheckOrderSerializer(serializers.Serializer):
    id = serializers.IntegerField
    price = serializers.IntegerField
    items = serializers.ListField
    address = serializers.StringRelatedField
    client = serializers.DictField
    point_id = serializers.IntegerField

    def create(self, validated_data):
        return Check(**validated_data)
