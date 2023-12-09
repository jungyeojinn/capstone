from django.shortcuts import render
from .models import Freight
from .serializers import FreightSerializer, FreightDetailSerializer
from quotes.models import Quote
from quotes.serializers import QuoteSerializer
from rest_framework.decorators import APIView
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from django.shortcuts import get_object_or_404

@permission_classes([IsAuthenticated])
class freight(APIView):
    @swagger_auto_schema(
        operation_description="포워더 사용자라면 등록되어 있는 모든 화물을 조회\n수출기업 사용자라면 해당 사용자의 화물만을 조회",
        operation_summary="화물 조회",
        tags=['freights'],
        responses={200: openapi.Response(description='화물 조회 성공', schema=FreightDetailSerializer(many=True))},
    )
    def get(self, request):     #화물 조회
        user=request.user
        if user.isForwarder == True:
            serializer =FreightDetailSerializer(Freight.objects.filter(isCompleted=False), many=True)
            return Response(serializer.data, status=200)      #포워더라면 등록되어 있는 화물 중 견적 수락이 완료되지 않은 화물을 모두 조회함
        else:
            userFreights = Freight.objects.filter(userId=request.user.userId)    #해당 사용자의 화물 모두 조회
            serializer = FreightSerializer(userFreights, many=True)
            return Response(serializer.data, status=200)
    
    @swagger_auto_schema(
        operation_description="화물 등록",
        operation_summary="화물 등록",
        tags=['freights'],
        request_body=FreightSerializer,
        responses={201: openapi.Response(description='화물 등록 성공')})
    def post(self,request):     #화물 등록
        serializer = FreightSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save(userId=request.user)    #화물 등록시 로그인한 사용자의 id를 저장
            request.user.totalItems += 1            #화물 등록시 사용자의 totalItems를 1 증가
            request.user.save()
            return Response(status=201)       

@permission_classes([IsAuthenticated])
class freight_detail(APIView):
    @swagger_auto_schema(
        operation_description="화물에 대한 견적 조회",
        operation_summary="화물에 대한 견적 조회",
        tags=['freights'],
        responses={200: openapi.Response(description='견적 조회 성공', schema=QuoteSerializer(many=True))})
    def get(self, request, freight_id):
        quote = Quote.objects.filter(freightId=freight_id)
        serializer = QuoteSerializer(quote, many=True)
        return Response(serializer.data, status=200)
    
    @swagger_auto_schema(
        operation_description="화물 삭제",
        operation_summary="화물 삭제",
        tags=['freights'],
        responses={200: openapi.Response(description='화물 삭제 성공'), 400: openapi.Response(description='화물 삭제 실패')})
    def delete(self, request, freight_id):  #화물 삭제
        user=request.user
        item = get_object_or_404(Freight, id=freight_id)
        if user == item.userId:  #삭제하려는 화물의 작성자가 로그인한 사용자와 같다면 삭제. 외래키로 연결된 객체를 직접 비교함
            item.delete()
            request.user.totalItems -= 1    #화물 삭제시 사용자의 totalItems를 1 감소
            request.user.save()
            return Response(status=200) #삭제 성공
        else:
            return Response(item.userId, status=400) #삭제 실패
