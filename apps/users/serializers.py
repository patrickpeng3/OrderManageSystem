from rest_framework import serializers
from apps.users.models import User


class UserSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)

    def create(self, validated_data):
        return User.objects.create(**validated_data)

    def update(self, instance, validated_data):
        