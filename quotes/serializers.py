from rest_framework import serializers
from .models import Quote
from freights.models import Freight

class QuoteListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Quote
        fields = ('id','freightId','shippingCompany','totalCharge','departureDate','arrivalDate','isFCL','content','created_at','updated_at','isAccepted',)

class QuoteSerializer(serializers.ModelSerializer): #견적 등록 시 사용 freightId를 외부에서 처리
    class Meta:
        model = Quote
        fields = ('shippingCompany','totalCharge','departureDate','arrivalDate','isFCL','content','created_at','updated_at','isAccepted',)