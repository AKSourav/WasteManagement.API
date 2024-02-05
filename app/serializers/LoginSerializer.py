# from rest_framework.serializers import serializers
from rest_framework import serializers
class LoginSerializer(serializers.Serializer):
    phone=serializers.CharField()
    password= serializers.CharField()