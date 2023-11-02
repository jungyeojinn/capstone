from django.shortcuts import render
from .models import Freight
from .serializers import FreightSerializer
from rest_framework.decorators import APIView
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

@permission_classes([IsAuthenticated])
class freight(APIView):    
    def get(self, request):     #조회
        user=request.user
        if user.isForwarder == False:
            return render('/')      #포워더가 아니라면 shipper 페이지로 리다이렉트
        else:
            userFreights = Freight.objects.filter(userId=request.user.id)    #해당 사용자의 화물 모두 조회
            serializer = FreightSerializer(userFreights, many=True)
            return Response(serializer.data)
    
    def post(self,request):     #생성
        serializer = FreightSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(status=201)
#         productName=request.data['productName'], width=request.data['width'], depth=request.data['depth'], height=request.data['height'], weight=request.data['weight'], quantity=request.data['quantity'], departureDate=request.data['departureDate'], arrivalDate=request.data['arrivalDate'], departurePlace=request.data['departurePlace'], arrivalPlace=request.data['arrivalPlace'], content=request.data.get['content'])
  #      newFreight.save()
  #      return Response({'message': '화물이 등록되었습니다.'})
    