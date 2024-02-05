from django.shortcuts import render,redirect
from django.views import View
from app.models import User,WasteCollectionPoint,WasteCollector,DistrictWasteCollector,StateWasteCollector
import random
from rest_framework.permissions import IsAuthenticated

# from django.http import JsonResponse, HttpResponse

from datetime import datetime

from rest_framework import status

from django.contrib.auth.hashers import make_password
from rest_framework.views import APIView

from rest_framework.response import Response
from rest_framework.decorators import api_view,permission_classes

from app.serializers.userSerializer import UserSerializer

from django.core.mail import send_mail,EmailMultiAlternatives
# from django.contrib import messages

from django.views.decorators.csrf import csrf_exempt

from app.serializers.WasteCollectionPointSerializer import WasteCollectionPointSerializer
from django.shortcuts import get_object_or_404

from django.db.models  import Q

import json



def unique_number(name):
    name=name
    while(True):  
        uq=random.randint(1000,9999)
        uq=name+str(uq)
        try:
            n=WasteCollectionPoint.objects.get(collection_point_id=uq)
        except:
            return uq
        
@permission_classes([IsAuthenticated]) 
class WasteCollectionPointAPI(APIView):
    def post(self, request):
        try:
            address=request.data.get('address')
            locality=request.data.get('locality')
            district=request.data.get('district')
            pincode=request.data.get('pincode')
            state=request.data.get('state')
            country=request.data.get('country')
            lattitude=request.data.get('lattitude')
            longitude=request.data.get('longitude')

            customer_ref=request.user
            collection_point_id=unique_number("coll")
            ab = WasteCollectionPoint.objects.create(customer_ref=customer_ref,collection_point_id=collection_point_id,optional_phone="none",address=address,locality=locality,district=district,pincode=pincode,state=state,country=country,lattitude=lattitude,longitude=longitude)

            try:
                optional_phone=request.data.get('optional_phone')
                ab.optional_phone=optional_phone
                ab.save()
                responseData= WasteCollectionPointSerializer(ab,many=False)
                return Response(responseData.data,status=status.HTTP_202_ACCEPTED)
            except:
                optional_phone=request.user.phone
                ab.optional_phone=optional_phone
                ab.save()
                responseData= WasteCollectionPointSerializer(ab,many=False)
                return Response(responseData.data,status=status.HTTP_202_ACCEPTED)
        except Exception as e:
            print(e)
            error_response = {
                'status': 400,
                'error': 'something_went_wrong',
                'message': 'Something went wrong',
                'data': {}
            }
            return Response(error_response, status=400)
        

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
                data = WasteCollectionPoint.objects.filter(
                        customer_ref=user,
                        **filter
                    )
            elif "WC" == user.user_type:
                roles = WasteCollector.objects.get(user_ref=user)
                data=WasteCollectionPoint.objects.filter(
                        Q(status="pending",district__iregex=roles.district_waste_collector_ref.district_level) | Q(status="accepted",waste_collector_ref=roles),
                        **filter
                    )
            elif "DWC" == user.user_type:
                roles = DistrictWasteCollector.objects.get(user_ref=user)
                data=WasteCollectionPoint.objects.filter(
                        Q(status="pending") | Q(status="accepted"),
                        district__iregex=roles.district_level,
                        **filter
                    )
            elif "SWC" == user.user_type:
                roles = StateWasteCollector.objects.get(user_ref=user)
                data=WasteCollectionPoint.objects.filter(
                        Q(status="pending") | Q(status="accepted"),
                        state__iregex=roles.state_level,
                        **filter
                    )
            
            if data is None:
                raise Exception("No Data")
            
            serializer = WasteCollectionPointSerializer(data,many=True)
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
          
   
# Update Addresss
@permission_classes([IsAuthenticated])
class WasteCollectionPointSlugAPI(APIView):
    def get(self,request,collection_point_id):
        try:
            collection_point = get_object_or_404(WasteCollectionPoint,collection_point_id=collection_point_id)
            responseData= WasteCollectionPointSerializer(collection_point,many=False).data
            print(responseData)
            return Response(responseData,status=status.HTTP_202_ACCEPTED)
        except Exception as e:
            print(e)
            error_response = {
                'status': 400,
                'error': 'something_went_wrong',
                'message': 'Something went wrong',
                'data': {}
            }
            return Response(error_response, status=400)

    def put(self,request,collection_point_id):
        try:
            date=request.data.get('date')
            slot_time=request.data.get('slot_time')
            user_ref=request.user.user_id
            waste_collector_ref= get_object_or_404(WasteCollector,user_ref=user_ref)
            collection_point = get_object_or_404(WasteCollectionPoint,collection_point_id=collection_point_id)
            collection_point.date=date
            collection_point.slot_time=slot_time
            collection_point.waste_collector_ref=waste_collector_ref
            collection_point.status="accepted"
            # print(collection_point.saved_address_ref)
            collection_point.save()
            responseData= WasteCollectionPointSerializer(collection_point,many=False).data
            return Response(responseData,status=status.HTTP_202_ACCEPTED)
        except Exception as e:
            print(e)
            error_response = {
                'status': 400,
                'error': 'something_went_wrong',
                'message': 'Something went wrong',
                'data': {}
            }
            return Response(error_response, status=400)
        
    def delete(self,request,collection_point_id):
        try:
            user_ref=request.user
            user_type=user_ref.user_type

            wp=WasteCollectionPoint.objects.get(Q(customer_ref=user_ref) | Q(waste_collector_ref__user_ref=user_ref),collection_point_id=collection_point_id)
            if wp.status in ["pending","accepted"] and wp.customer_ref==user_ref:
                wp.status = "cancel"
                wp.updated_by=request.user
                wp.save()
                serializerInstance= WasteCollectionPointSerializer(wp,many=False)
                print(serializerInstance.data)
                return Response(serializerInstance.data,status=status.HTTP_202_ACCEPTED)
            if wp.status in ["accepted"] and wp.waste_collector_ref.user_ref==user_ref:
                wp.status = "pending"
                wp.waste_collector_ref=None
                wp.slot_time=None
                wp.date=None
                wp.updated_by=request.user
                wp.save()
                serializerInstance= WasteCollectionPointSerializer(wp,many=False)
                print(serializerInstance.data)
                return Response(serializerInstance.data,status=status.HTTP_202_ACCEPTED)
            error_response = {
                'status': 400,
                'error': 'something_went_wrong',
                'message': 'Something went wrong',
                'data': {}
            }
            return Response(error_response, status=400)
        except Exception as e:
            print(e)
            error_response = {
                'status': 400,
                'error': 'something_went_wrong',
                'message': 'Something went wrong',
                'data': {}
            }
            return Response(error_response, status=400)

    







