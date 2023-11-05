from django.shortcuts import render
from rest_framework.decorators import APIView, permission_classes
from rest_framework.permissions import IsAuthenticated
from .models import Quote
from freights.models import Freight
from .serializers import QuoteSerializer, QuoteListSerializer
from rest_framework.response import Response
from django.shortcuts import get_object_or_404

@permission_classes([IsAuthenticated])
class quotes(APIView):
    def get(self, request):     #자신이 등록한 견적 조회
        user=request.user
        if user.isForwarder == True:
            userQuotes = Quote.objects.filter(userId=request.user.userId)    #해당 사용자의 견적 모두 조회
            serializer = QuoteListSerializer(userQuotes, many=True)
            return Response(serializer.data)        #포워더라면 자신이 등록한 화물을 조회함
        else:
            return Response(status=403)             #수출기업 사용자라면 조회할 수 없음

    def post(self, request, freightId):     #견적 등록
        freight = get_object_or_404(Freight, pk=freightId)
        data=request.data
        serializer = QuoteSerializer(data=request.data) #freightId를 context로 넘겨줌
        if serializer.is_valid(raise_exception=True):
            serializer.save(userId=request.user, freightId=freight)    #견적 등록시 로그인한 사용자의 id를 저장
            return Response(status=201)