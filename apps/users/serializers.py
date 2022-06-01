from rest_framework import serializers
from apps.users.models import User


class UserSerializer(serializers.ModelSerializer):
    # id = serializers.IntegerField(read_only=True)
    # name = serializers.CharField(required=False, allow_blank=True, max_length=50)
    # number = serializers.CharField(required=False, allow_blank=True, max_length=11)
    # email = serializers.CharField(required=True, max_length=100)
    # gender = serializers.CharField(max_length=6)
    # city = serializers.CharField(required=False, allow_blank=True, max_length=100)
    # score = serializers.IntegerField(required=False)
    # school = serializers.CharField(required=False, allow_blank=True, max_length=100)
    # add_time = serializers.DateTimeField(required=True)
    #
    # def create(self, validated_data):
    #     return User.objects.create(**validated_data)
    #
    # def update(self, instance, validated_data):
    #     instance.name = validated_data.get('name', instance.name)
    #     instance.number = validated_data.get('number', instance.number)
    #     instance.email = validated_data.get('email', instance.email)
    #     instance.gender = validated_data.get('gender', instance.gender)
    #     instance.city = validated_data.get('city', instance.city)
    #     instance.score = validated_data.get('score', instance.score)
    #     instance.school = validated_data.get('school', instance.school)
    #     instance.add_time = validated_data.get('add_time', instance.add_time)
    #     instance.save()
    #     return instance

    class Meta:
        model = User
        fields = ('id', 'name', 'number', 'email', 'gender', 'city', 'score', 'school', 'add_time')
