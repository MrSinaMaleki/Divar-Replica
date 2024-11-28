from django.shortcuts import render
from rest_framework.views import APIView
from apps.account.serializers import UserLoginSerializer
from rest_framework.views import APIView
from django.conf import settings
from django.contrib.auth import get_user_model
from rest_framework import exceptions
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework.decorators import api_view, permission_classes
from django.shortcuts import redirect
from django.core.cache import cache
from random import randint
from django.contrib.auth import authenticate, login
from django.urls import reverse_lazy
from django.core.mail import send_mail
from django.views import View
# from services.mail import MailProvider

# Create your views here.

class SignRegister(APIView):
    permission_classes = [AllowAny, ]
    serializer_class = UserLoginSerializer

    @staticmethod
    def code_generator():
        return str(randint(100_000, 999999))

    def post(self, request, *args, **kwargs):
        email = request.data.get('email')
        if email is None:
            return Response({'Message': 'Invalid Email'}, status=401)

        if not (code := cache.get(email)):
            code = self.code_generator()

        print(code)
        cache.set(email, code, 180)
        return Response({"status": "success"})


class Verify(APIView):
    permission_classes = [AllowAny, ]
    serializer_class = UserLoginSerializer

    def post(self, request, *args, **kwargs):
        email = request.data.get('email')
        response = Response()

        if email is None:
            return Response({'Message': 'Invalid Email'}, status=401)

        code = request.data.get("code")
        if code is None:
            return Response({'Message': 'Invalid Code'}, status=401)

        if cache.get(email) != code:
            return Response({'Message': 'Code has been expired'}, status=401)

        User = get_user_model()

        user, created = User.objects.get_or_create(email=email)
        login(request, user)

        serialized_user = self.serializer_class(user).data
        response.data = {
            'message': 'logged in successfully',
            'user': serialized_user,
        }
        return response



# test








