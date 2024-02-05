from django.shortcuts import render,redirect,HttpResponse
import random
# from app.models import Patient,Appointment,Department
from django.contrib import messages
from app.models import WasteCollector,DistrictWasteCollector,StateWasteCollector,User

from rest_framework.views import APIView
   
from rest_framework.response import Response
from rest_framework.decorators import api_view,permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.serializers import ListSerializer, ValidationError

from app.serializers.userSerializer import UserSerializer,UserWasteCollectorSerializer,UserDistrictCollectorSerializer,UserStateCollectorSerializer

import json
from urllib.parse import unquote


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def GetPersonalDetails(request):
    try:
        user= request.user
        serializer = UserSerializer(user,many= False)
        print(serializer.data)
        return Response({"user":serializer.data})
    except Exception as e:
        print("GetUser ERR",e)
        return Response({"messages":"Error"},status=500)

def getUserByType(user_ref, filter):
    DWC = {
        "state_waste_collector_ref__user_ref": user_ref
    }

    WC = {
        "district_waste_collector_ref__state_waste_collector_ref__user_ref": user_ref
    }
    USER = {
        "user_type":"USER"
    }
    ResponseData = []

    # UserDistrictCollectorSerializer
    DWCdata = UserDistrictCollectorSerializer(DistrictWasteCollector.objects.filter(**DWC, **filter), many=True)
    ResponseData += DWCdata.data

    # UserWasteCollectorSerializer
    WCdata = UserWasteCollectorSerializer(WasteCollector.objects.filter(**WC, **filter), many=True)
    ResponseData += WCdata.data

    # UserSerializer with ListSerializer
    user_list = User.objects.filter(**USER, **filter)
    print(user_list)
    Userdata = UserSerializer(user_list, many=True)
    ResponseData += list(Userdata.data)

    return ResponseData

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def GetUserALL(request):
    try:
        # print("params",type(request.query_params.get("name")))
        # Get the encoded filter from the query parameters
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

        ResponseData=getUserByType(request.user,decoded_filter)
        return Response(ResponseData)
    
    except Exception as e:
        print("Error", e)
        error_response = {
            'status': 500,
            'error': 'something_went_wrong',
            'message': 'Internal server error',
            'data': {}
        }
        return Response(error_response, status=500)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def GetUserWasteCollector(request):
    try:
        # print("params",type(request.query_params.get("name")))
        # Get the encoded filter from the query parameters
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
        
        # if 'SWC'==request.user.user_type:

        # Filter based on the decoded filter
        data_queryset = WasteCollector.objects.filter(**decoded_filter)
        print("data_queryset:", data_queryset)

        # Serialize the queryset
        serializer = UserWasteCollectorSerializer(data=data_queryset, many=True)
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
    

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def GetUserDistrictCollector(request):
    try:
        # print("params",type(request.query_params.get("name")))
        # Get the encoded filter from the query parameters
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
        data_queryset = DistrictWasteCollector.objects.filter(**decoded_filter)
        print("data_queryset:", data_queryset)

        # Serialize the queryset
        serializer = UserDistrictCollectorSerializer(data=data_queryset, many=True)
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
    

@api_view(['GET'])
@permission_classes([IsAuthenticated]) 
class GetUser(APIView):
    def get(self, request):
        try:
            # print("params",type(request.query_params.get("name")))
            # Get the encoded filter from the query parameters
            encoded_filter = request.query_params.get('filter', None)
            decoded_filter = {}
            print("1",decoded_filter)
            try:
                # Decode and parse the JSON filter
                decoded_filter = json.loads(unquote(encoded_filter))
                print("2",decoded_filter)
            except:
                decoded_filter = {}
                print("3",decoded_filter)



            # Check if the decoded filter is a dictionary
            if not isinstance(decoded_filter, dict):
                decoded_filter={}
                print("4",decoded_filter)
            
             # Filter based on the decoded filter
            data_queryset = User.objects.filter(**decoded_filter)

            # Serialize the queryset
            serializer = UserSerializer(data=data_queryset, many=True)
            serializer.is_valid()  # Call .is_valid() before accessing .data
            serialized_data = serializer.data  # Access the serialized data

            # Print or do something with the serialized data

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
    


@permission_classes([IsAuthenticated]) 
class GetWasteCollector(APIView):
    def get(self, request):
        try:
            # print("params",type(request.query_params.get("name")))
            # Get the encoded filter from the query parameters
            encoded_filter = request.query_params.get('filter', None)
            decoded_filter = {}
            print("1",decoded_filter)
            try:
                # Decode and parse the JSON filter
                decoded_filter = json.loads(unquote(encoded_filter))
                print("2",decoded_filter)
            except:
                decoded_filter = {}
                print("3",decoded_filter)



            # Check if the decoded filter is a dictionary
            if not isinstance(decoded_filter, dict):
                decoded_filter={}
                print("4",decoded_filter)
            
             # Filter based on the decoded filter
            data_queryset = WasteCollector.objects.filter(**decoded_filter)

            # Serialize the queryset
            serializer = UserWasteCollectorSerializer(data=data_queryset, many=True)
            serializer.is_valid()  # Call .is_valid() before accessing .data
            serialized_data = serializer.data  # Access the serialized data

            # Print or do something with the serialized data

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
    

@permission_classes([IsAuthenticated]) 
class GetDistrictWasteCollector(APIView):
    def get(self, request):
        try:
            # print("params",type(request.query_params.get("name")))
            # Get the encoded filter from the query parameters
            encoded_filter = request.query_params.get('filter', None)
            decoded_filter = {}
            print("1",decoded_filter)
            try:
                # Decode and parse the JSON filter
                decoded_filter = json.loads(unquote(encoded_filter))
                print("2",decoded_filter)
            except:
                decoded_filter = {}
                print("3",decoded_filter)



            # Check if the decoded filter is a dictionary
            if not isinstance(decoded_filter, dict):
                decoded_filter={}
                print("4",decoded_filter)
            
             # Filter based on the decoded filter
            data_queryset = DistrictWasteCollector.objects.filter(**decoded_filter)

            # Serialize the queryset
            serializer = UserDistrictCollectorSerializer(data=data_queryset, many=True)
            serializer.is_valid()  # Call .is_valid() before accessing .data
            serialized_data = serializer.data  # Access the serialized data

            # Print or do something with the serialized data

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
    
