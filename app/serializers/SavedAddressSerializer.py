from rest_framework import serializers
from app.models import SavedAddress

class SavedAddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = SavedAddress
        fields = '__all__'


class UpdateSavedAddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = SavedAddress
        exclude = ['saved_address_id', 'customer_ref']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Set required=False for all fields except excluded ones
        for field_name, field in self.fields.items():
            if field_name not in self.Meta.exclude:
                field.required = False