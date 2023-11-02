from django.shortcuts import render
from .models import Freight
from .serializers import FreightSerializer
from rest_framework.decorators import APIView
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

@permission_classes([IsAuthenticated])
class freight(APIView):    
    def get(self, request):     #화물 조회
        user=request.user
        if user.isForwarder == True:
            serializer = FreightSerializer(Freight.objects.all(), many=True)
            return Response(serializer.data)      #포워더라면 등록되어 있는 모든 화물을 조회함
        else:
            userFreights = Freight.objects.filter(userId=request.user.userId)    #해당 사용자의 화물 모두 조회
            serializer = FreightSerializer(userFreights, many=True)
            return Response(serializer.data)
    
    def post(self,request):     #화물 등록
        serializer = FreightSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save(userId=request.user)    #화물 등록시 로그인한 사용자의 id를 저장
            return Response(status=201)
