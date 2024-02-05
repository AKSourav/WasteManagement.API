from rest_framework import serializers
from app.models import WasteCollectionRecord,WasteTypeDetail

class WasteCollectionRecordSerializer(serializers.ModelSerializer):
    class Meta:
        model = WasteCollectionRecord
        fields = '__all__'


class WasteTypeDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = WasteTypeDetail
        fields = '__all__'