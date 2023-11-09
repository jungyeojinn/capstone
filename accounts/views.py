from django.shortcuts import render
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes #@permission_classes ([AllowAny]) 데코레이션 추가하여 해당 뷰에 접근할 때 인증 절차를 거치지 않도록 함
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from .serializers import userSerializer
from rest_framework.decorators import APIView
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.renderers import JSONRenderer
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
import jwt, datetime
from .models import User
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

# Swagger API 문서화를 위한 데코레이터
@swagger_auto_schema(
  operation_description="회원가입",
  operation_summary="회원가입",
  tags=['accounts'],
  methods=['post'], 
  request_body=userSerializer, 
  response_body=userSerializer)
@api_view(['POST'])
@permission_classes([AllowAny])
def signup(request):
  "회원가입"
  serializer = userSerializer(data=request.data)
  if serializer.is_valid(raise_exception=True):
      user = serializer.save()
      user.set_password(request.data.get('password'))
      user.save()
      return Response(serializer.data, status=status.HTTP_201_CREATED)


@permission_classes([AllowAny])
class login(APIView) :
  @swagger_auto_schema(
  operation_description="로그인",
  operation_summary="로그인",
  tags=['accounts'],
  request_body=openapi.Schema(
    type=openapi.TYPE_OBJECT,
    properties={
      'userId': openapi.Schema(type=openapi.TYPE_STRING, description='아이디'),
      'password': openapi.Schema(type=openapi.TYPE_STRING, description='비밀번호')}
  ),
  responses={200: openapi.Response(description='로그인 성공',
    schema=openapi.Schema(
      type=openapi.TYPE_OBJECT,
      properties={
          "userType" : openapi.Schema(type=openapi.TYPE_BOOLEAN, description='포워더 여부'),
          "token": openapi.Schema(type=openapi.TYPE_STRING, description='토큰')})
  )})
  def post(self,request):
    userId = request.data['userId']
    password = request.data['password']

    user = User.objects.filter(userId=userId).first()
    serialize_user = userSerializer(user)
    usertype = serialize_user.data['isForwarder']

    # 아이디와 비밀번호 일치 확인
    if user is None or not user.check_password(password):
      raise AuthenticationFailed("아이디 또는 비밀번호를 잘못 입력했습니다.")
	
    ## JWT
    token = TokenObtainPairSerializer.get_token(user)
    access_token = str(token.access_token)
    res = Response(
      {
        "userType" : usertype,
        "token": access_token,
      },
      status=status.HTTP_200_OK,
    )
    return res