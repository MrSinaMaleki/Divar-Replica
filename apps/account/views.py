from mimetypes import read_mime_types

from apps.account.serializers import UserLoginSerializer, UserVerifySerializer
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from random import randint
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.tokens import RefreshToken, TokenError
from django.core.cache import cache
from rest_framework.exceptions import AuthenticationFailed
from django.contrib.auth import get_user_model, login
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from django.contrib.auth import login, logout
from django.shortcuts import redirect
from apps.account.models import User
from rest_framework import status
from rest_framework import generics
from apps.post.serializers import AllPostsSerializer
from apps.post.models import Post
from django.shortcuts import get_object_or_404
from apps.account.tasks import send_email

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


        send_email.delay(
            subject="Login/Register CODE",
            recipient=email,
            template="mail/code.html",
            context={"code": code}
        )

        # _ = MailProvider(
        #     "Login/Register CODE",
        #     email,
        #     "mail/code.html",
        #     {"code": code}
        # ).send()

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
    permission_classes = []
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

        login(request, user)
        tokens = self.get_tokens_for_user(user)

        response = Response({
            'message': 'Logged in successfully',
        })
        response.set_cookie(
            key='access',
            value=tokens['access'],
        )

        response.set_cookie(
            key='refresh',
            value=tokens['refresh'],
        )

        return response


# class TokenRefreshView(APIView):
#     permission_classes = [AllowAny, ]
#     def post(self, request, *args, **kwargs):
#         refresh_token = request.COOKIES.get('refresh_token')
#
#         if not refresh_token:
#             return Response({'message': 'Refresh token not found'}, status=400)
#
#         try:
#             refresh = RefreshToken(refresh_token)
#             new_access_token = str(refresh.access_token)
#
#             response = Response({'message': 'Access token refreshed successfully'})
#             response.set_cookie(
#                 key='access_token',
#                 value=new_access_token,
#                 httponly=True,
#                 samesite='Lax',
#             )
#             return response
#         except TokenError:
#             raise AuthenticationFailed('Invalid or expired refresh token')



def logout_view(request):
    logout(request)
    return redirect('/')


class VerifyCheck(APIView):
    serializer_class = UserVerifySerializer

    def get(self, request, *args, **kwargs):
        try:
            user = User.objects.get(id=request.user.id)
            return Response({
                "is_verified": user.is_verified,
                "is_verified_date": user.is_verified_date
            }, status=status.HTTP_200_OK)

        except User.DoesNotExist:
            return Response({'Message': 'User does not exist'}, status=status.HTTP_404_NOT_FOUND)


    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            # print('request.data: ',request.data)
            # print('request.user: ',request.user.id)

            user_id = request.user.id
            nationality = serializer.validated_data['nationality']
            id_number = serializer.validated_data['id_number']

            try:
                user = User.objects.get(id=user_id)

                if nationality not in dict(User.Nationalities.choices):
                    return Response({"error": "Invalid nationality."}, status=status.HTTP_400_BAD_REQUEST)

                if len(id_number) != 11 or not id_number.isdigit():
                    return Response({"error": "ID number must be 11 digits."}, status=status.HTTP_400_BAD_REQUEST)

                user.nationality = nationality
                user.id_number = id_number
                user.waiting_verified = True
                # user.is_verified_date = now()
                user.save()

                return Response({"message": "User verification successful."}, status=status.HTTP_200_OK)

            except User.DoesNotExist:
                return Response({"error": "User with this email does not exist."}, status=status.HTTP_404_NOT_FOUND)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



from rest_framework.generics import RetrieveUpdateAPIView
from apps.account.serializers import UserSerializer
class Profile(RetrieveUpdateAPIView):
    serializer_class = UserSerializer
    queryset = User.objects.all()


class UserPosts(generics.ListAPIView):
    serializer_class = AllPostsSerializer

    def get_queryset(self):
        user = self.request.user
        posts = Post.objects.filter(user=user)
        return posts


class DelPost(APIView):
    def post(self, request, *args, **kwargs):
        post_id = request.data.get('post_id')
        if not post_id:
            return Response({"error": "Post ID is required."}, status=status.HTTP_400_BAD_REQUEST)

        post = get_object_or_404(Post, id=post_id)


        if post.user != request.user and not request.user.is_staff:
            return Response(
                {"error": "You do not have permission to delete this post."},
                status=status.HTTP_403_FORBIDDEN
            )


        post.make_delete()

        # Return a success response
        return Response({"message": "Post deleted successfully."}, status=status.HTTP_200_OK)


class OtherUserPosts(generics.ListAPIView):
    permission_classes = [AllowAny]
    serializer_class = AllPostsSerializer

    def get_queryset(self):
        user_id = self.request.query_params.get('user_id')
        if user_id is not None:
            posts = Post.objects.filter(user_id=user_id)
            return posts
        return Post.objects.none()
