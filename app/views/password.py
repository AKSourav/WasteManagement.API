from django.shortcuts import render,redirect
from django.views import View
from app.models import User

from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView


from rest_framework import status

from django.contrib.auth.hashers import make_password

from rest_framework.response import Response
from rest_framework.decorators import api_view,permission_classes

from app.serializers.userSerializer import UserSerializer
from app.serializers.WasteCollectionRecordSerializer import WasteCollectionRecordSerializer

from django.core.mail import send_mail,EmailMultiAlternatives
# from django.contrib import messages

from django.views.decorators.csrf import csrf_exempt


class ForgetPasswordAPI(APIView):
    def post(self, request):
        try:
            
            phone=request.data.get('phone')
            password=request.data.get('password')
            password = make_password(password)
            try:
                ab=User.objects.get(phone=phone)
                ab.password=password
                ab.save()
                return Response({"message":'Password Change Successful !'},status=status.HTTP_202_ACCEPTED)     

            except Exception as e:
                        error_response = {
                            'status': 400,
                            'error': 'something_went_wrong',
                            'message': 'Register Phone number not found',
                            'data': {}
                        }
                        return Response(error_response, status=400)

        except Exception as e:
            error_response = {
                'status': 400,
                'error': 'something_went_wrong',
                'message': 'Forget Password section',
                'data': {}
            }
            return Response(error_response, status=400)
        
@permission_classes([IsAuthenticated]) 
class UpdatePasswordAPI(APIView):
    def put(self, request):
        try:
            
            phone=request.user.phone
            password = make_password(password)
            user=User.objects.get(phone=phone)
            user.password=password
            user.save()
            return Response({"message":'Password Change Successful !'},status=status.HTTP_202_ACCEPTED)     

        except Exception as e:
            error_response = {
                'status': 400,
                'error': 'something_went_wrong',
                'message': 'Update Password section',
                'data': {}
            }
            return Response(error_response, status=400)
 




