from rest_framework.serializers import ModelSerializer,SerializerMethodField
from app.models import WasteCollectionPoint,SavedAddress


# class WasteCollectionPointSerializer(ModelSerializer):
#     # Define a SerializerMethodField for the phone field
#     customer_email = SerializerMethodField()
#     customer_first_name = SerializerMethodField()
#     customer_last_name = SerializerMethodField()
#     waste_collector_firstname = SerializerMethodField()
#     waste_collector_lastname = SerializerMethodField()
#     waste_collector_phone = SerializerMethodField()

#     class Meta:
#         model = WasteCollectionPoint
#         fields = ['address','date','slot_time','status', 'city','pincode','state','country','optional_phone','customer_email','customer_first_name','customer_last_name','waste_collector_firstname','waste_collector_lastname','waste_collector_phone','lattitude','longitude']

#     # Define a method to get the customer_phone field value
#     def get_collection_address(self, obj):
#         # Access the related model's customer_phone field
#         if obj.saved_address_ref:
#             return obj.saved_address_ref.address
#         return None
    
#     def get_collection_city(self, obj):
#         # Access the related model's customer_phone field
#         if obj.saved_address_ref:
#             return obj.saved_address_ref.city
#         return None
    
#     def get_collection_pincode(self, obj):
#         # Access the related model's customer_phone field
#         if obj.saved_address_ref:
#             return obj.saved_address_ref.pincode
#         return None
#     def get_collection_state(self, obj):
#         # Access the related model's customer_phone field
#         if obj.saved_address_ref:
#             return obj.saved_address_ref.state
#         return None
#     def get_collection_country(self, obj):
#         # Access the related model's customer_phone field
#         if obj.saved_address_ref:
#             return obj.saved_address_ref.country
#         return None
#     def get_collection_longitude(self, obj):
#         # Access the related model's customer_phone field
#         if obj.saved_address_ref:
#             return obj.saved_address_ref.longitude
#         return None
#     def get_collection_lattitude(self, obj):
#         # Access the related model's customer_phone field
#         if obj.saved_address_ref:
#             return obj.saved_address_ref.lattitude
#         return None


#     def get_customer_email(self, obj):
#         # Access the related model's customer_email field
#         if obj.customer_ref:
#             return obj.customer_ref.email
#         return None
#     def get_customer_first_name(self, obj):
#         # Access the related model's customer_first_name field
#         if obj.customer_ref:
#             return obj.customer_ref.first_name
#         return None
#     def get_customer_last_name(self, obj):
#         # Access the related model's customer_last_name field
#         if obj.customer_ref:
#             return obj.customer_ref.last_name
#         return None
    

#     # Waste collector ref.......................
#     def get_waste_collector_firstname(self, obj):
#         # Access the related model's waste_collector_firstname field
#         if obj.waste_collector_ref:
#             return obj.waste_collector_ref.user_ref.first_name
#         return None
    
#     def get_waste_collector_lastname(self, obj):
#         # Access the related model's waste_collector_lastname field
#         if obj.waste_collector_ref:
#             return obj.waste_collector_ref.user_ref.last_name
#         return None

#     def get_waste_collector_phone(self, obj):
#         # Access the related model's waste_collector_phone field
#         if obj.waste_collector_ref:
#             return obj.waste_collector_ref.user_ref.phone
#         return None




from rest_framework import serializers
from app.models import SavedAddress, WasteCollectionPoint

# class WasteCollectionPointSerializer(serializers.ModelSerializer):
#     lattitude = serializers.CharField(source='saved_address_ref.lattitude', read_only=True)
#     city = serializers.CharField(source='saved_address_ref.district', read_only=True)
#     # Add other fields from SavedAddress as needed

#     class Meta:
#         model = WasteCollectionPoint
#         exclude = ['saved_address_ref']





class SavedAddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = SavedAddress
        fields = '__all__'

class WasteCollectionPointSerializer(serializers.ModelSerializer):

    class Meta:
        model = WasteCollectionPoint
        fields = '__all__'