from apps.account.serializers import UserLoginSerializer
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from random import randint
# from services.mail import MailProvider
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.tokens import RefreshToken, TokenError
from django.core.cache import cache
from rest_framework.exceptions import AuthenticationFailed
from django.contrib.auth import get_user_model, login
# Create your views here.

class SignRegister(APIView):
    """
     - example request

        {

            "email": "user@example.com",

        }

    """
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

        # _ = MailProvider(
        #     "Login/Register CODE",
        #     email,
        #     "mail/code.html",
        #     {"code": code}
        # ).send()

        print(code)
        cache.set(email, code, 180)
        return Response({"status": "success"})


class Verify(APIView):
    """
     - example request

        {

            "email": "user@example.com",
            "code": "code"

        }

    """
    permission_classes = [AllowAny, ]
    serializer_class = UserLoginSerializer

    def get_tokens_for_user(self, user):

        refresh = RefreshToken.for_user(user)
        return {
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }


    def post(self, request, *args, **kwargs):
        email = request.data.get('email')
        code = request.data.get("code")
        response = Response()

        if email is None:
            return Response({'Message': 'Invalid Email'}, status=401)

        if code is None:
            return Response({'Message': 'Invalid Code'}, status=401)

        if cache.get(email) != code:
            return Response({'Message': 'Code has been expired'}, status=401)

        User = get_user_model()
        user, created = User.objects.get_or_create(email=email)

        # login(request, user)
        tokens = self.get_tokens_for_user(user)

        response = Response({
            'message': 'Logged in successfully',
        })
        response.set_cookie(
            key='access_token',
            value=tokens['access'],
            httponly=True,
            # secure=settings.DEBUG is False,  # Use secure cookies in production
            samesite='Lax',
        )
        response.set_cookie(
            key='refresh_token',
            value=tokens['refresh'],
            httponly=True,
            # secure=settings.DEBUG is False,  # Use secure cookies in production
            samesite='Lax',
        )
        return response


class TokenRefreshView(APIView):
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        refresh_token = request.COOKIES.get('refresh_token')

        if not refresh_token:
            return Response({'message': 'Refresh token not found'}, status=400)

        try:
            refresh = RefreshToken(refresh_token)
            new_access_token = str(refresh.access_token)

            response = Response({'message': 'Access token refreshed successfully'})
            response.set_cookie(
                key='access_token',
                value=new_access_token,
                httponly=True,
                # secure=settings.DEBUG is False,
                samesite='Lax',
            )
            return response
        except TokenError:
            raise AuthenticationFailed('Invalid or expired refresh token')


class Profile(APIView):
    def get(self, request, *args, **kwargs):
        return Response({"Pofile": "Bla bla bla ...!"})
