from rest_framework import serializers
from .models import Freight

class FreightSerializer(serializers.ModelSerializer):
    class Meta:
        model = Freight
        fields = ('productName', 'width', 'depth', 'height', 'weight', 'quantity', 'departureDate', 'arrivalDate', 'departurePlace', 'arrivalPlace', 'content',)