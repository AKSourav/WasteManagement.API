from rest_framework.serializers import ModelSerializer
from app.models import User, WasteCollector,DistrictWasteCollector,StateWasteCollector
from rest_framework import serializers

class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        exclude = ['password', 'delete']


class UserWasteCollectorSerializer(ModelSerializer):
    user_ref = UserSerializer()
    class Meta:
        model = WasteCollector
        fields = '__all__'

class UserDistrictCollectorSerializer(ModelSerializer):
    user_ref = UserSerializer()
    class Meta:
        model = DistrictWasteCollector
        fields = '__all__'



class UserStateCollectorSerializer(ModelSerializer):
    user_ref = UserSerializer()
    class Meta:
        model = StateWasteCollector
        fields = '__all__'


