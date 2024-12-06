from rest_framework import serializers
from apps.account.models import User


class UserLoginSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['email']
