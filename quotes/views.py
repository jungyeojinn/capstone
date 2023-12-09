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
from django.core.mail import EmailMessage
from django.template.loader import render_to_string #email 전송 위해 추가
from django.core.mail import EmailMultiAlternatives
from django.contrib.staticfiles import finders
import base64




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
        operation_description="견적등록. 견적이 등록된 화물을 가진 수출기업 사용자에게 견적이 등록되었음을 알리는 메일 전송",
        operation_summary="견적 등록",
        tags=['quotes'],
        request_body=QuoteSerializer,
        manual_parameters=[openapi.Parameter("freightId", openapi.IN_QUERY, type=openapi.TYPE_INTEGER, description="freightId")],
        response={201: openapi.Response(description='견적 등록 성공')})
    def post(self, request):     #견적 등록
        freightId = request.data['freightId']
        freight = get_object_or_404(Freight, pk=freightId)
        serializer = QuoteSerializer(data=request.data) 

        #견적이 등록되었음을 알리는 메일 전송
        image_path = finders.find("quotes\logo.png")
        with open(image_path, 'rb') as img_file:
            image_data = base64.b64encode(img_file.read()).decode('utf-8')
        htmlContent = render_to_string("quote/mail.html", {'image_data': image_data, 'product':freight.productName})
        email = EmailMultiAlternatives(
            '견적이 등록되었습니다.',       # 제목
            htmlContent,       # 내용
            to=[freight.userId.email],  # 등록한 견적의 화물 소유자에게 이메일 전송
        )
        email.attach_alternative(htmlContent, "text/html")
        email.send()
        if serializer.is_valid(raise_exception=True):
            request.user.totalItems += 1    #견적 등록시 사용자의 totalItems 1 증가
            serializer.save(userId=request.user, freightId=freight)    #견적 등록시 로그인한 사용자의 id를 저장, freightId를 context로 넘겨줌
            request.user.save()
            return Response(status=201)
    
    @swagger_auto_schema(
        operation_description="견적 수정. 일부 필드만 수정 가능. parameter로 'shippingCompany','totalCharge','departureDate','arrivalDate','isFCL','content' 중 수정할 내용만 전송",
        operation_summary="견적 수정",
        tags=['quotes'],
        #swagger가 partial을 지원하지 않음
        requst_body=QuoteSerializer,                  
        response={200: openapi.Response(description='견적 수정 성공')}
    )
    def patch(self, request):      #견적 수정
        quoteId = request.data['quoteId']
        quote = get_object_or_404(Quote, pk=quoteId)
        serializer = QuoteSerializer(quote, data=request.data, partial=True)        # partial=True로 설정하여 전체 필드가 아닌 일부 필드만 수정 가능하게 함
        if(serializer.is_valid(raise_exception=True)):
            serializer.save()
            return Response(status=200)

@permission_classes([IsAuthenticated])
class accept(APIView):
    @swagger_auto_schema(
        operation_description="수락된 견적 조회",
        operation_summary="자신이 등록한 견적 중 수락된 견적 조회",
        tags=['quotes'],
        responses={200: openapi.Response(description='견적 조회 성공', schema=QuoteListSerializer(many=True)), 400: openapi.Response(description='포워더 사용자가 아니라면 조회할 수 없음')}
    )
    def get(self, request):     #포워딩 업체 사용자가 등록한 견적 중 수출기업에 의해 수락된 견적을 조회할 수 있음
        user=request.user
        if user.isForwarder == True:
            userQuotes = Quote.objects.filter(userId=request.user.userId, isAccepted=True)                      #해당 사용자의 견적 중 수락된 견적을 모두 조회
            serializer = QuoteListSerializer(userQuotes, many=True)
            return Response(serializer.data, status=200)        #포워더 사용자라면 자신이 수락한 견적을 조회함
        else:
            return Response(status=403)             #수출기업 사용자라면 조회할 수 없음
    
    @swagger_auto_schema(
    operation_description="견적 수락. 견적을 등록한 포워더에게 견적이 수락되었음을 알리는 메일 전송",
    operation_summary="견적 수락",
    tags=['quotes'],
    request_body=openapi.Schema(type=openapi.TYPE_INTEGER, property={'quoteId': '견적 id'}),
    response={200: openapi.Response(description='견적 수락 성공')}
    )
    def patch(self, request):      #견적 수락
        quoteId = request.data['quoteId']
        quote = get_object_or_404(Quote, pk=quoteId)
        freight = get_object_or_404(Freight, pk=quote.freightId.pk)
        freight.isCompleted = True  #해당 견적에 연결된 화물의 isCompleted 플래그를 True로 바꿈
        freight.save()
        quote.isAccepted = True
        quote.save()
        
        #견적이 수락되었음을 알리는 메일 전송
        image_path = finders.find("quotes\logo.png")
        with open(image_path, 'rb') as img_file:
            image_data = base64.b64encode(img_file.read()).decode('utf-8')
        htmlContent = render_to_string("quote/mail.html", {'image_data': image_data, 'product':freight.productName})
        email = EmailMultiAlternatives(
            '견적이 수락되었습니다.',       # 제목
            htmlContent,       # 내용
            to=[quote.userId.email],  # 등록한 견적의 화물 소유자에게 이메일 전송
        )
        email.attach_alternative(htmlContent, "text/html")
        email.send()
        return Response(status=200)

@permission_classes([IsAuthenticated])
class quote_detail(APIView):    
    @swagger_auto_schema(
        operation_description="견적 삭제",
        operation_summary="견적 삭제",
        tags=['quotes'],
        responses={200: openapi.Response(description='견적 삭제 성공'), 400: openapi.Response(description='견적 삭제 실패')})
    def delete(self,request,quote_id):   #견적 삭제
        user=request.user
        item = get_object_or_404(Quote, id=quote_id)  #파라미터로 넘어온 quoteId를 가진 화물을 찾음
        if user.userId == item.userId:
            item.delete()
            request.user.totalItems -= 1    #견적 삭제시 사용자의 totalItems 1 감소
            request.user.save()
            return Response(status=200) #삭제 성공
        else:
            return Response(status=400) #삭제 실패