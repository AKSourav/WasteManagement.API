from django.shortcuts import render,redirect
from django.views import View
from app.models import User,WasteCollectionRecord,WasteCollectionPoint,WasteCollector,Wallet
import random
# from django.http import JsonResponse, HttpResponse
from django.db.models import Sum

from datetime import datetime

from rest_framework import status

from django.contrib.auth.hashers import make_password

from rest_framework.response import Response
from rest_framework.decorators import api_view,permission_classes

from app.serializers.userSerializer import UserSerializer

from django.core.mail import send_mail,EmailMultiAlternatives
# from django.contrib import messages
from rest_framework.permissions import IsAuthenticated

from django.views.decorators.csrf import csrf_exempt

from rest_framework.views import APIView


  

@permission_classes([IsAuthenticated]) 
class CreditAPI(APIView):
    def post(self, request):
        try:
            user = request.user
            order_id=request.data.get('order_id')
            payment_id=request.data.get('payment_id')
            transaction_amount=request.data.get('transaction_amount')
            credit_transactions=request.data.get('credit_transactions')
            debit_transactions=request.data.get('debit_transactions')

            ab = Wallet.objects.create(user_ref=user,order_id=order_id,payment_id=payment_id,transaction_amount=transaction_amount,credit_transactions=credit_transactions,debit_transactions=debit_transactions)
            ad=WasteCollectionRecord.objects.get(order_id=order_id)
            ad.payment_status="done"
            ad.save()
            return Response({"message":'Credit Successfully'},status=status.HTTP_202_ACCEPTED)     
            
        except:
            ad=WasteCollectionRecord.objects.get(order_id=order_id)
            ad.payment_status="failed"
            ad.save()
            
            return Response({"message":'Payment failed'},status=status.HTTP_400_BAD_REQUEST)     


          


@permission_classes([IsAuthenticated]) 
class DebitAPI(APIView):
    def post(self, request):
        try:
            user = request.user
            total_credits = Wallet.objects.get(user_ref=user, payment_type="credits").aggregate(Sum('money'))['money__sum'] or 0
            total_debits = Wallet.objects.get(user_ref=user, payment_type="debits").aggregate(Sum('money'))['money__sum'] or 0
            balance = total_credits - total_debits

            if balance > 50:
                withdraw = float(request.data.get('withdraw'))
                new_balance = balance - withdraw
                order_id = request.data.get('order_id')
                payment_id = request.data.get('payment_id')
                re=Wallet.objects.create(user_ref=user,order_id=order_id, payment_id=payment_id,payment_type="debit", money=withdraw, balance=new_balance)
                
                return Response({"message": 'Withdraw Successfully'}, status=status.HTTP_200_OK)
            else:
                return Response({"message": 'Your Balance Is Low'}, status=status.HTTP_200_OK)


        except Wallet.DoesNotExist:
            error_response = {
                'status': 404,
                'error': 'wallet_not_found',
                'message': 'Wallet not found for the user',
                'data': {}
            }
            return Response(error_response, status=404)
        except Exception as e:
            error_response = {
                'status': 400,
                'error': 'something_went_wrong',
                'message': 'Something went wrong',
                'data': {}
            }
            return Response(error_response, status=400)





