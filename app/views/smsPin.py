from django.views import View
from app.models import User,WasteCollector,WasteCollectionPoint
import random

from rest_framework import status

from rest_framework.response import Response
from rest_framework.decorators import api_view,permission_classes

from app.serializers.userSerializer import UserSerializer

from django.core.mail import send_mail,EmailMultiAlternatives
# from django.contrib import messages
from rest_framework.permissions import IsAuthenticated


from rest_framework.views import APIView

from django.template.loader import render_to_string




@permission_classes([IsAuthenticated]) 
class SmsPinAPI(APIView):
    optMapping={}
    def get(self,request,collection_point_id):
         try:
            user=request.user
            data=request.query_params
            collection_point_id=data.get('collection_point_id',collection_point_id)
            expectedOTP=self.optMapping.get((user.user_id,collection_point_id))
            otp=data['otp']
            print("expected:",expectedOTP)
            print("otp:",otp)
            if str(expectedOTP) != str(otp):
                raise Exception('Invalid Otp')
            return Response({"message":"success"},status=status.HTTP_201_CREATED) 
         except Exception as e:
            print(e)
            error_response = {
                'status': 400,
                'error': 'something_went_wrong',
                'message': 'Invalid OTP',
                'data': {}
            }
            
            return Response({"message":error_response},status=status.HTTP_400_BAD_REQUEST)
    
    def post(self, request,collection_point_id):
        try:
            user=request.user
            data=request.data
            collection_point_id=data['collection_point_id']
            cp=WasteCollectionPoint.objects.get(collection_point_id=collection_point_id,waste_collector_ref__user_ref=user)
            if not cp:
                 raise Exception('Invalid Operation for a user/ Collection Point Invalid')
            user_email=cp.customer_ref.email

            items= request.data.get('items',None)
            if items == None or len(items)==0:
                 raise Exception('No Items added!')
            
            # Calculate total price
            total_cost = sum(float(item['total_cost']) for item in items)
            pin =mail(items,total_cost,user_email)

            self.optMapping[(user.user_id,collection_point_id)]=pin
            print(str(self.optMapping))
            return Response({"message":"success"},status=status.HTTP_201_CREATED)     

        except Exception as e:
            print(e)
            error_response = {
                'status': 400,
                'error': 'something_went_wrong',
                'message': 'SMS Failed',
                'data': {}
            }
            
            return Response({"message":error_response},status=status.HTTP_400_BAD_REQUEST)     





def mail(items,total_price,email):
    try:
        subject = 'PIN COMFORMATION'
        from_email = 'mastikipathshala828109@gmail.com'

        # Correct template_path and render the HTML template with the provided data
        template_path = 'emailtem.html'
        pin=random.randint(9999,99999)
        context = {'pin': pin,
                'items':items,
                'total_price':total_price,
                }
        message = render_to_string(template_path, context)

        to = "anupdevil2001@gmail.com"

        msg = EmailMultiAlternatives(subject, '', from_email, [to])
        msg.attach_alternative(message, 'text/html')
        msg.send()
        return pin
    except Exception as e:
            print("smg errr:",e)
            raise Exception("Prob")