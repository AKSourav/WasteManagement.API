from rest_framework.response import Response
from rest_framework.decorators import api_view


a=0

@api_view(['GET'])
def testFun(request):
    global a
    a+=1
    return Response({"message":a})