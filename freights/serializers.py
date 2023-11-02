from rest_framework import serializers
from .models import Freight

class FreightSerializer(serializers.ModelSerializer):
    class Meta:
        model = Freight
        fields = ('userId','productName', 'width', 'depth', 'height', 'weight', 'quantity', 'departureDate', 'arrivalDate', 'departurePlace', 'arrivalPlace', 'content',)
        