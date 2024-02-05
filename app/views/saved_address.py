from rest_framework.views import APIView
from app.models import SavedAddress
from app.serializers.SavedAddressSerializer import SavedAddressSerializer,UpdateSavedAddressSerializer
from rest_framework.decorators import api_view,permission_classes
import random
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from rest_framework.response import Response
from django.shortcuts import get_object_or_404

def unique_number(name):
    name=name
    while(True):  
        uq=random.randint(1000,9999)
        uq=name+str(uq)
        try:
            n=SavedAddress.objects.get(collection_point_id=uq)
        except:
            return uq
        

@permission_classes([IsAuthenticated])
class SavedAddressAPI(APIView):

    def post(self, request):
        try:
            address=request.data.get('address')
            district=request.data.get('district')
            pincode=request.data.get('pincode')
            state=request.data.get('state')
            country=request.data.get('country')
            lattitude=request.data.get('lattitude')
            longitude=request.data.get('longitude')
            locality=request.data.get('locality')
            customer_ref=request.user
            saved_address_id=unique_number("loc")
            newAddress = SavedAddress.objects.create(customer_ref=customer_ref,address=address,saved_address_id=saved_address_id,district=district,pincode=pincode,state=state,country=country,lattitude=lattitude,longitude=longitude,locality=locality)
            
            responseData= SavedAddressSerializer(newAddress).data
            # print(responseData)
            return Response(responseData,status=status.HTTP_202_ACCEPTED)
            # return Response({"message":'Address Saved !'},status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            # print( e)
            error_response = {
                'status': 400,
                'error': 'something_went_wrong',
                'message': 'Something went wrong',
                'data': {}
            }
            return Response(error_response, status=400)
    def get(self,request):

        try:
            user_id = request.user
            saved_addresses = SavedAddress.objects.filter(customer_ref=user_id)
            responseData= SavedAddressSerializer(saved_addresses,many=True).data
            return Response(responseData,status=status.HTTP_202_ACCEPTED)
        except Exception as e:
            # print(e)
            error_response = {
                'status': 400,
                'error': 'something_went_wrong',
                'message': 'Something went wrong',
                'data': {}
            }
            return Response(error_response, status=400)
        
# Update Addresss
@permission_classes([IsAuthenticated])
class SavedAddressSlugAPI(APIView):
    def put(self,request,saved_address_id):
        try:
            user_id = request.user.user_id
    
            serializer = UpdateSavedAddressSerializer(data=request.data)
            if serializer.is_valid():
                print("ser",serializer.validated_data)

                SavedAddress.objects.filter(customer_ref=user_id,saved_address_id=saved_address_id).update(**serializer.validated_data)
                responseData=SavedAddress.objects.filter(customer_ref=user_id,saved_address_id=saved_address_id).first()
                print("respose",responseData)

                responseData= SavedAddressSerializer(responseData,many=False).data
                return Response(responseData,status=status.HTTP_202_ACCEPTED)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
                raise ValueError('Invalid Update Operation')

        except Exception as e:
            print(e)
            error_response = {
                'status': 400,
                'error': 'something_went_wrong',
                'message': 'Something went wrong',
                'data': {}
            }
            return Response(error_response, status=400)
        
    def delete(self,request,saved_address_id):
        try:
            user_id=request.user
            SavedAddress.objects.filter(customer_ref=user_id, saved_address_id=saved_address_id).delete()
            return Response({"message":"Success","id":saved_address_id},status=status.HTTP_202_ACCEPTED)
        except Exception as e:
            print(e)
            error_response = {
                'status': 400,
                'error': 'something_went_wrong',
                'message': 'Something went wrong',
                'data': {}
            }
            return Response(error_response, status=400)