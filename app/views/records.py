import cloudinary
import cloudinary.uploader
from rest_framework.response import Response

from rest_framework.decorators import permission_classes
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from app.models import WasteTypeDetail,WasteCollectionRecord,WasteCollectionPoint, WasteCollector, StateWasteCollector, DistrictWasteCollector
from app.serializers.WasteCollectionRecordSerializer import WasteCollectionRecordSerializer, WasteTypeSerializer

import json
import random

def unique_number(name):
    name=name
    while(True):  
        uq=random.randint(1000,9999)
        uq=name+str(uq)
        try:
            n=WasteCollectionRecord.objects.get(record_id=uq)
        except:
            return uq

@permission_classes([IsAuthenticated]) 
class WasteCollectionRecordAPI(APIView):
    def post(self,request,collection_point_id):

        print("Completing WC Point with "+collection_point_id)
        try:
            user=request.user
            if(user.user_type!="WC"):
                raise Exception("Not Valid")
            print(request.POST)
            waste_items = []
            total_price=0
            collection_point_ref= WasteCollectionPoint.objects.get(collection_point_id=collection_point_id)
            print("Holla:",collection_point_ref)
            recordTuple, created = WasteCollectionRecord.objects.update_or_create(
                defaults={'collection_point_ref': collection_point_ref},
            )
            print("Here:",WasteCollectionRecordSerializer(recordTuple,many=False).data)
            # return Response({"message":collection_point_ref.collection_point_id},status=200)
            for index in range(len(request.FILES)):
                image = request.FILES[f'image{index}']
                price = request.POST[f'price{index}']
                total_cost = request.POST[f'total_cost{index}']
                waste_type = request.POST[f'waste_type{index}']
                weight = request.POST[f'weight{index}']

                # Upload image to Cloudinary
                result = cloudinary.uploader.upload(image, folder='waste_images')
                print("Cloudinary Result:",str(result))
                # Get the public ID of the uploaded image from Cloudinary
                # cloudinary_public_id = result['public_id']
                url_cloudinary=result['url']

                # Create WasteItem instance with Cloudinary public ID
                waste_item={
                    "waste_type":waste_type,
                    "price":float(price),
                    "weight":float(weight),
                    "total_cost":float(total_cost),
                    "image":url_cloudinary
                }
                print("waste:",str(waste_item))
                total_price+=float(total_cost)
                waste_items.append(waste_item)
                wasteItem= WasteTypeDetail.objects.create(record_ref=recordTuple,**waste_item)
                print(wasteItem)
            recordTuple.total_price = float(total_price) or 0.0
            print("Here2:",WasteCollectionRecordSerializer(recordTuple,many=False).data)
            recordTuple.save()        
            return Response(WasteCollectionRecordSerializer(recordTuple,many=False).data, status=200)
        except Exception as e:
            print(e)
            return Response({'error': 'Invalid request method'}, status=400)
    
    

@permission_classes([IsAuthenticated]) 
class RecordsAPI(APIView):
    def get(self, request):
        print("Hola")
        try:
            user=request.user
            # Getting filter
            filter=request.query_params.get("filter")
            try:
                filter=json.loads(filter)
            except:
                filter={}
            print(filter)
            data = None
            if "USER" == user.user_type:  
                data = WasteCollectionRecord.objects.filter(
                        collection_point_ref__customer_ref=user
                    )
            elif "WC" == user.user_type:
                roles = WasteCollector.objects.get(user_ref=user)
                data=WasteCollectionRecord.objects.filter(
                        collection_point_ref__waste_collector_ref=roles,
                        **filter
                    )
            elif "DWC" == user.user_type:
                roles = DistrictWasteCollector.objects.get(user_ref=user)
                data=WasteCollectionRecord.objects.filter(
                        collection_point_ref__district__iregex=roles.district_level,
                        **filter
                    )
            elif "SWC" == user.user_type:
                roles = StateWasteCollector.objects.get(user_ref=user)
                data=WasteCollectionRecord.objects.filter(
                        collection_point_ref__state__iregex=roles.state_level,
                        **filter
                    )
            
            if data is None:
                raise Exception("No Data")
            
            serializer = WasteCollectionRecordSerializer(data,many=True)
            return Response(serializer.data)
            
        except Exception as e:
            print(f"An error occurred: {e}")
            error_response = {
                'status': 404,
                'error': 'records_not_found',
                'message': 'No records found for the user',
                'data': {}
            }
            return Response(error_response, status=404)
 
@permission_classes([IsAuthenticated]) 
class RecordsInfoAPI(APIView):
    def get(self, request,record_id):
        try:
            user=request.user
            # Getting filter
            filter=request.query_params.get("filter")
            try:
                filter=json.loads(filter)
            except:
                filter={}
            print(filter)
            data = None
            if "USER" == user.user_type:  
                data = WasteCollectionRecord.objects.get(
                        collection_point_ref__customer_ref=user,
                        record_id=record_id
                    )
            elif "WC" == user.user_type:
                roles = WasteCollector.objects.get(user_ref=user)
                data=WasteCollectionRecord.objects.get(
                        collection_point_ref__waste_collector_ref=roles,
                        record_id=record_id,
                        **filter
                    )
            elif "DWC" == user.user_type:
                roles = DistrictWasteCollector.objects.get(user_ref=user)
                data=WasteCollectionRecord.objects.get(
                        collection_point_ref__district__iregex=roles.district_level,
                        record_id=record_id,
                        **filter
                    )
            elif "SWC" == user.user_type:
                roles = StateWasteCollector.objects.get(user_ref=user)
                data=WasteCollectionRecord.objects.get(
                        collection_point_ref__state__iregex=roles.state_level,
                        record_id=record_id,
                        **filter
                    )
            
            if data is None:
                raise Exception("No Data")
            print(data)
            serializer = WasteCollectionRecordSerializer(data,many=False)
            return Response(serializer.data)
            
        except Exception as e:
            print(f"An error occurred: {e}")
            error_response = {
                'status': 404,
                'error': 'records_not_found',
                'message': 'No records found for the user',
                'data': {}
            }
            return Response(error_response, status=404)
        
@permission_classes([IsAuthenticated]) 
class ItemInfoAPI(APIView):
    def get(self, request,record_id):
        try:
            user=request.user
            # Getting filter
            filter=request.query_params.get("filter")
            try:
                filter=json.loads(filter)
            except:
                filter={}
            print(filter)
            data = None
            if "USER" == user.user_type:  
                data = WasteTypeDetail.objects.filter(
                        record_ref__collection_point_ref__customer_ref=user,
                        record_ref__record_id=record_id
                    )
            elif "WC" == user.user_type:
                roles = WasteCollector.objects.get(user_ref=user)
                data=WasteTypeDetail.objects.filter(
                        record_ref__collection_point_ref__waste_collector_ref=roles,
                        record_ref__record_id=record_id,
                        **filter
                    )
            elif "DWC" == user.user_type:
                roles = DistrictWasteCollector.objects.get(user_ref=user)
                data=WasteTypeDetail.objects.filter(
                        record_ref__collection_point_ref__district__iregex=roles.district_level,
                        record_ref__record_id=record_id,
                        **filter
                    )
            elif "SWC" == user.user_type:
                roles = StateWasteCollector.objects.get(user_ref=user)
                data=WasteTypeDetail.objects.filter(
                        record_ref__collection_point_ref__state__iregex=roles.state_level,
                        record_ref__record_id=record_id,
                        **filter
                    )
            
            if data is None:
                raise Exception("No Data")
            print(data)
            serializer = WasteTypeSerializer(data,many=True)
            return Response(serializer.data)
            
        except Exception as e:
            print(f"An error occurred: {e}")
            error_response = {
                'status': 404,
                'error': 'records_not_found',
                'message': 'No records found for the user',
                'data': {}
            }
            return Response(error_response, status=404)
 
