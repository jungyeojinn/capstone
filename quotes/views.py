from django.shortcuts import render
from rest_framework.decorators import APIView, permission_classes
from rest_framework.permissions import IsAuthenticated
from .models import Quote
from freights.models import Freight
from .serializers import QuoteSerializer, QuoteListSerializer
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from rest_framework.decorators import api_view

@permission_classes([IsAuthenticated])
class quotes(APIView):
    @swagger_auto_schema(
        operation_description="견적 조회",
        operation_summary="견적 조회",
        tags=['quotes'],
        responses={200: openapi.Response(description='화물 조회 성공',schema=QuoteListSerializer(many=True)),
                   403: openapi.Response(description='수출기업 사용자라면 조회할 수 없음')}
    )
    def get(self, request):     #자신이 등록한 견적 조회
        user=request.user
        if user.isForwarder == True:
            userQuotes = Quote.objects.filter(userId=request.user.userId)    #해당 사용자의 견적 모두 조회
            serializer = QuoteListSerializer(userQuotes, many=True)
            return Response(serializer.data, status=200)        #포워더라면 자신이 등록한 화물을 조회함
        else:
            return Response(status=403)             #수출기업 사용자라면 조회할 수 없음

    @swagger_auto_schema(
        operation_description="견적 등록",
        operation_summary="견적 등록",
        tags=['quotes'],
        request_body=QuoteSerializer,
        manual_parameters=[openapi.Parameter("freightId", openapi.IN_QUERY, type=openapi.TYPE_INTEGER, description="freightId")],
        response={201: openapi.Response(description='견적 등록 성공')})
    def post(self, request):     #견적 등록
        freightId = request.data['freightId']
        freight = get_object_or_404(Freight, pk=freightId)
        data=request.data
        serializer = QuoteSerializer(data=request.data) 
        if serializer.is_valid(raise_exception=True):
            serializer.save(userId=request.user, freightId=freight)    #견적 등록시 로그인한 사용자의 id를 저장, freightId를 context로 넘겨줌
            return Response(status=201)
    
    @swagger_auto_schema(
        operation_description="견적 수락",
        operation_summary="견적 수락",
        tags=['quotes'],
        request_body=openapi.Schema(type=openapi.TYPE_INTEGER, property={'quoteId': '견적 id'}),
        response={200: openapi.Response(description='견적 수락 성공')}
    )
    def patch(self, request):      #견적 수락
        quoteId = request.data['quoteId']
        quote = get_object_or_404(Quote, pk=quoteId)
        quote.isAccepted = True
        quote.save()
        return Response(status=200)

@permission_classes([IsAuthenticated])
class accepted_quotes(APIView):
    @swagger_auto_schema(
        operation_description="수락된 견적 조회",
        operation_summary="자신이 등록한 견적 중 수락된 견적 조회",
        tags=['quotes'],
        response={200: openapi.Response(description='견적 조회 성공', schema=QuoteListSerializer(many=True)), 400: openapi.Response(description='포워더 사용자가 아니라면 조회할 수 없음')}
    )
    def get(self, request):     #포워딩 업체 사용자가 등록한 견적 중 수출기업에 의해 수락된 견적을 조회할 수 있음
        user=request.user
        if user.isForwarder == True:
            userQuotes = Quote.objects.filter(userId=request.user.userId, isAccepted=True)    #해당 사용자의 견적 중 수락된 견적을 모두 조회
            serializer = QuoteListSerializer(userQuotes, many=True)
            return Response(serializer.data, status=200)        #포워더 사용자라면 자신이 수락한 견적을 조회함
        else:
            return Response(status=403)             #수출기업 사용자라면 조회할 수 없음