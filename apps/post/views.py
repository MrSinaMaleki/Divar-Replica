from apps.post.models import Post
from rest_framework import generics
from rest_framework.permissions import AllowAny
from .serializers import PostSerializer
from rest_framework.views import APIView
from rest_framework.response import Response

class AddPostView(APIView):
    permission_classes = (AllowAny,)
