from rest_framework import serializers
from .models import Freight

class FreightSerializer(serializers.ModelSerializer):
    userId = serializers.CharField(read_only=True)      #POST 요청시 userId는 자동으로 저장되도록 함
    id = serializers.CharField(read_only=True)          #POST 요청시 화물id는 자동으로 생성됨
    class Meta:
        model = Freight
        fields = ('id','userId','productName', 'width', 'depth', 'height', 'weight', 'quantity', 'departureDate', 'arrivalDate', 'departurePlace', 'arrivalPlace', 'content',)
        