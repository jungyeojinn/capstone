from django.shortcuts import render
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes #@permission_classes ([AllowAny]) 데코레이션 추가하여 해당 뷰에 접근할 때 인증 절차를 거치지 않도록 함
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from .serializers import userSerializer

@api_view(['POST'])
@permission_classes([AllowAny])
def signup(request):
    serializer = userSerializer(data=request.data)
    if serializer.is_valid(raise_exception=True):
        user = serializer.save()
        user.set_password(request.data.get('password'))
        user.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
