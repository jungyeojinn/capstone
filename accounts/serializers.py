from rest_framework import serializers
from django.contrib.auth import get_user_model


class userSerializer(serializers.ModelSerializer):

    class Meta:
        model = get_user_model()
        fields = ('userId', 'password', 'name', 'companyName', 'contact', 'email', 'isForwarder',)
