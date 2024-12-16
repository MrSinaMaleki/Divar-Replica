from django.shortcuts import render
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status
from rest_framework.generics import ListCreateAPIView
from apps.bookmark.serializer import FavoriteAddSerializer
from apps.bookmark.models import Bookmark
from rest_framework.views import APIView

class FavoriteAddView(ListCreateAPIView):
    serializer_class = FavoriteAddSerializer

    def get(self, request, *args, **kwargs):
        user = self.request.user
        post = self.request.query_params.get('post', None)
        exist= Bookmark.objects.filter(user_id=user.id, posts=post, is_active=True).exists()
        return Response({'exists': exist})


class MyLikedPosts(APIView):
    pass