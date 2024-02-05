from django.shortcuts import render,redirect
from django.views import View
from app.models import User,WasteCollector,DistrictWasteCollector,StateWasteCollector
import random
# from django.http import JsonResponse, HttpResponse

from datetime import datetime

from rest_framework import status

from django.contrib.auth.hashers import make_password

from rest_framework.response import Response
from rest_framework.decorators import api_view,permission_classes

from app.serializers.userSerializer import UserSerializer

from django.core.mail import send_mail,EmailMultiAlternatives
# from django.contrib import messages

from django.views.decorators.csrf import csrf_exempt
from rest_framework.views import APIView

        
        
def unique_number(ref):
    name=ref
    while(True):  
        uq=random.randint(1000,9999)
        uq=name+str(uq)
        try:
            if 'WC' == ref:
                n=WasteCollector.objects.get(waste_collector_id=uq)
            elif 'DWC' == ref : 
                n=DistrictWasteCollector.objects.get(district_waste_collector_id=uq)
            elif 'SWC' == ref :
                n=StateWasteCollector.objects.get(state_waste_collector_id=uq)
            else :
                n=User.objects.get(user_id=uq)


        except:
            return uq


class RegisterAPI(APIView):
    def post(self, request):
        try:
            # Extract common user information
            first_name = request.data.get('first_name')
            last_name = request.data.get('last_name')
            email = request.data.get('email')
            phone = request.data.get('phone')
            password = request.data.get('password')
            try:
                user=User.objects.get(phone=phone)
                return Response({"message":'Already Register !'},status=status.HTTP_400_BAD_REQUEST)
            except:

                user_type = request.data.get('user_type')
                user_id = unique_number("US")
                password = make_password(password)

                if user_type == 'WC':
                    # Handle Waste Collector registration
                    return self.register_waste_collector(request, user_id, phone, email, password, first_name, last_name)

                elif user_type == 'DWC':
                    # Handle District Waste Collector registration
                    return self.register_district_waste_collector(request, user_id, phone, email, password, first_name, last_name)

                elif user_type == 'SWC':
                    # Handle State Waste Collector registration
                    return self.register_state_waste_collector(request, user_id, phone, email, password, first_name, last_name)

                else:
                    # Handle regular User registration
                    return self.register_user(request, user_id, phone, email, password, first_name, last_name)

        except Exception as e:
            print(e)
            error_response = {
                'status': 400,
                'error': 'something_went_wrong',
                'message': 'Something went wrong',
                'data': {}
            }
            return Response(error_response, status=400)

    def register_waste_collector(self, request, user_id, phone, email, password, first_name, last_name):
        try:
            waste_collector_id = unique_number("WC")
            district_waste_collector_id = request.data.get('district_waste_collector_id')
            district_waste_collector_ref = DistrictWasteCollector.objects.get(district_waste_collector_id=district_waste_collector_id)
            
            user_ref = User.objects.create(user_id=user_id, phone=phone, email=email, password=password, first_name=first_name, last_name=last_name, user_type='WC', blood_group=request.data.get('blood_group'), gender=request.data.get('gender'), age=request.data.get('age'))
            
            wc = WasteCollector.objects.create(waste_collector_id=waste_collector_id, user_ref=user_ref, district_waste_collector_ref=district_waste_collector_ref)
            
            return Response({"message": 'saved Successfully'}, status=status.HTTP_201_CREATED)

        except Exception as e:
            error_response = {
                'status': 400,
                'error': 'something_went_wrong',
                'message': 'User Type WC Section',
                'data': {}
            }
            return Response(error_response, status=400)
        
    def register_district_waste_collector(self, request, user_id, phone, email, password, first_name, last_name):
        try:
            district_waste_collector_id=unique_number("DWC")
            state_waste_collector_id=request.data.get('state_waste_collector_id')
            state_waste_collector_ref = StateWasteCollector.objects.get(state_waste_collector_id=state_waste_collector_id)
            user_ref = User.objects.create(user_id=user_id, phone=phone, email=email, password=password, first_name=first_name, last_name=last_name, user_type='DWC', blood_group=request.data.get('blood_group'), gender=request.data.get('gender'), age=request.data.get('age'))
            
            ba = DistrictWasteCollector.objects.create(user_ref=user_ref,district_level=request.data.get('district_level'),state_waste_collector_ref=state_waste_collector_ref,district_waste_collector_id=district_waste_collector_id)
            
            return Response({"message": 'saved Successfully'}, status=status.HTTP_201_CREATED)

        except Exception as e:
            print(e)
            error_response = {
                'status': 400,
                'error': 'something_went_wrong',
                'message': 'User Type DWC Section',
                'data': {}
            }
            return Response(error_response, status=400)


    def register_state_waste_collector(self, request, user_id, phone, email, password, first_name, last_name):
        try:
            state_waste_collector_id=unique_number("SWC")
            user_ref = User.objects.create(user_id=user_id, phone=phone, email=email, password=password, first_name=first_name, last_name=last_name, user_type='SWC', blood_group=request.data.get('blood_group'), gender=request.data.get('gender'), age=request.data.get('age'))
            ba = StateWasteCollector.objects.create(user_ref=user_ref,state_level=request.data.get('state_level'),state_waste_collector_id=state_waste_collector_id)
 
            return Response({"message": 'saved Successfully'}, status=status.HTTP_201_CREATED)

        except Exception as e:
            error_response = {
                'status': 400,
                'error': 'something_went_wrong',
                'message': 'User Type SWC Section',
                'data': {}
            }
            return Response(error_response, status=400)

    def register_user(self, request, user_id, phone, email, password, first_name, last_name):
        try:
            user_ref = User.objects.create(user_id=user_id, phone=phone, email=email, password=password, first_name=first_name, last_name=last_name, user_type='USER')
                        
            return Response({"message": 'saved Successfully'}, status=status.HTTP_201_CREATED)

        except Exception as e:
            print(e)
            error_response = {
                'status': 400,
                'error': 'something_went_wrong',
                'message': 'User Type USER Section',
                'data': {}
            }
            return Response(error_response, status=400)

