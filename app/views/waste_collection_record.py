from django.shortcuts import render,redirect
from django.views import View
from app.models import User,WasteCollectionRecord,WasteCollectionPoint,WasteCollector,WasteTypeDetail
import random
# from django.http import JsonResponse, HttpResponse
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView

from datetime import datetime

from rest_framework import status

from django.contrib.auth.hashers import make_password

from rest_framework.response import Response
from rest_framework.decorators import api_view,permission_classes

from app.serializers.userSerializer import UserSerializer
from app.serializers.WasteCollectionRecordSerializer import WasteCollectionRecordSerializer

from django.core.mail import send_mail,EmailMultiAlternatives
# from django.contrib import messages

from django.views.decorators.csrf import csrf_exempt

import json
from urllib.parse import unquote


def unique_number(name):
    name=name
    while(True):  
        uq=random.randint(1000,9999)
        uq=name+str(uq)
        try:
            n=WasteCollectionRecord.objects.get(record_id=uq)
        except:
            return uq
        
from django.db.models import FilteredRelation, Q

  
# @permission_classes([IsAuthenticated]) 
class WasteCollectionRecordAPI(APIView):

    def post(self, request):
        try:
            collection_point_id = request.data.get('collection_point_id')
            record_id = unique_number("record")
            order_id = unique_number("order")
            collection_point_ref = WasteCollectionPoint.objects.get(collection_point_id=collection_point_id)
            ab = WasteCollectionRecord.objects.create(record_id=record_id, order_id=order_id, collection_point_ref=collection_point_ref)
            
            waste_type_data_list = [
                ('plastic', 'quantity_plastic', 'plastic_pay'),
                ('iron', 'quantity_iron', 'iron_pay'),
                ('glass', 'quantity_glass', 'glass_pay'),
                ('paper', 'quantity_paper', 'paper_pay')
            ]

            for waste_type, quantity_key, pay_key in waste_type_data_list:
                try:
                    waste_type_value = request.data.get(waste_type)
                    quantity_collected_value = request.data.get(quantity_key)
                    pay_value = request.data.get(pay_key)

                    WasteTypeDetail.objects.create(record_ref=ab, waste_type=waste_type_value,
                                                quantity_collected=quantity_collected_value, pay=pay_value)
                except:
                    pass

        # Move the return statement outside the loop
            return Response({"message": 'saved Successfully'}, status=status.HTTP_202_ACCEPTED)


        except Exception as e:
            error_response = {
                'status': 400,
                'error': 'something_went_wrong',
                'message': 'Something went wrong',
                'data': {}
            }
            return Response(error_response, status=400)

    def get(self, request):
        try:
            
            encoded_filter = request.query_params.get('filter', None)
            decoded_filter = {}
            try:
                # Decode and parse the JSON filter
                decoded_filter = json.loads(unquote(encoded_filter))
            except:
                decoded_filter = {}

            print("decoded_filter",decoded_filter)

            # Check if the decoded filter is a dictionary
            if not isinstance(decoded_filter, dict):
                decoded_filter={}
            # Filter based on the decoded filter
            data_queryset = WasteCollectionRecord.objects.filter(**decoded_filter)

            # Serialize the queryset
            serializer = WasteCollectionRecordSerializer(data=data_queryset, many=True)
            serializer.is_valid()  # Call .is_valid() before accessing .data
            serialized_data = serializer.data  # Access the serialized data

            # Print or do something with the serialized data
            print("serialized_data:", serialized_data)

            return Response({"message": serialized_data})
        except Exception as e:
            print("Error", e)
            error_response = {
                'status': 500,
                'error': 'something_went_wrong',
                'message': 'Internal server error',
                'data': {}
            }
        return Response(error_response, status=500)


        # try:
        #     user=request.user

        #     try:   
        #         data = WasteCollectionRecord.objects.filter(collection_point_ref__customer_ref=user)
                
        #     except WasteCollectionRecord.DoesNotExist:
        #         error_response = {
        #             'status': 404,
        #             'error': 'records_not_found',
        #             'message': 'No records found for the user',
        #             'data': {}
        #         }
        #         return Response(error_response, status=404)

        #     serializer = WasteCollectionRecordSerializer(data,many=True)
        #     return Response(serializer.data)
        # except Exception as e:
        #     error_response = {
        #         'status': 500,
        #         'error': 'something_went_wrong',
        #         'message': 'Internal server error',
        #         'data': {}
        #     }
        #     return Response(error_response, status=500)
          



