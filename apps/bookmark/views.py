from django.shortcuts import render
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status
from rest_framework.generics import ListCreateAPIView
from apps.bookmark.serializer import FavoriteAddSerializer, MyFavoriteSerializer
from rest_framework.views import APIView
from apps.bookmark.models import Bookmark

class FavoriteAddView(ListCreateAPIView):
    serializer_class = FavoriteAddSerializer

    def get(self, request, *args, **kwargs):
        user = self.request.user
        post = self.request.query_params.get('post', None)
        exist= Bookmark.objects.filter(user_id=user.id, posts=post, is_active=True).exists()
        return Response({'exists': exist})


class MyLikedPosts(APIView):
    serializer_class = MyFavoriteSerializer

    def get(self, request, *args, **kwargs):
        user = self.request.user
        # Fetch the bookmarks for the user
        bookmarks = Bookmark.objects.filter(user_id=user.id)

        # Pass the queryset as the instance, not data
        serializer = self.serializer_class(bookmarks, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

