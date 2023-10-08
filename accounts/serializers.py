from rest_framework import serializers
from django.contrib.auth import get_user_model

class userSerializer(serializers.ModelSerializer):
#    password = serializers.CharField(write_only=True)

    class Meta:
        model = get_user_model()
        fields = ('userId', 'password', 'userName', 'companyName', 'contact', 'email', 'isForwarder',)
