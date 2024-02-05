from django.shortcuts import render,redirect
from django.views import View
from app.models import User
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


@permission_classes([IsAuthenticated]) 
class UpdateProfileAPI(APIView):
    def put(self, request):
        try:
            
            phone=request.user.phone
            ab=User.objects.get(phone=phone)
            ab.first_name = request.data.get('first_name')
            ab.last_name = request.data.get('last_name')
            ab.age = request.data.get('age')
            ab.gender = request.data.get('gender')
            ab.blood_group = request.data.get('blood_group')
            ab.save()
            return Response({"message":'Profile Update Successfully'},status=status.HTTP_202_ACCEPTED)     
    
        except Exception as e:
            error_response = {
                'status': 400,
                'error': 'something_went_wrong',
                'message': 'Not Update',
                'data': {}
            }
            return Response(error_response, status=400)
        



