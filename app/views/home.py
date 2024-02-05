from django.shortcuts import render,redirect,HttpResponse
import random
# from app.models import Patient,Appointment,Department
from django.contrib import messages
from app.models import StateWasteCollector

   
from rest_framework.response import Response
from rest_framework.decorators import api_view,permission_classes
from rest_framework.permissions import IsAuthenticated

from app.serializers.userSerializer import UserSerializer,UserStateCollectorSerializer

def index(request):
    # return render(request,'home/index.html')
    return render(request,'Site Maintenance.html')

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def getUser(request):
    user= request.user
    serializer = UserSerializer(user,many= False)
    print(serializer.data)
    return Response({"user":serializer.data})


@api_view(['GET'])
def getUserStateCollector(request):
    try:
        filter = {'state_level': "Jharkhand"}
        data_queryset = StateWasteCollector.objects.filter(**filter)

        # Convert QuerySet to a list
        data_list = list(data_queryset)
        print("data",data_list)
        # Serialize the data
        serializer = UserStateCollectorSerializer(data=data_list, many=True)
        
        # Validate the serializer
        serializer.is_valid(raise_exception=True)
        
        # Access the serialized data
        return Response({"message": serializer.data})
    except Exception as e:
        print("Error", e)
        error_response = {
            'status': 500,
            'error': 'something_went_wrong',
            'message': 'Internal server error',
            'data': {}
        }
        return Response(error_response, status=500)
