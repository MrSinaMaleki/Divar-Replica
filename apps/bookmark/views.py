from django.shortcuts import render
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from apps.bookmark.serializer import BookMarkSerializer
from apps.bookmark.models import Bookmark

# Create your views here.
class BookMarkCreateListView(APIView):
    serializer_class = BookMarkSerializer
    """
    Viewing and adding more post
    """
    def get(self, request, *args, **kwargs):
        user = request.user
        bookmark = Bookmark.objects.filter(user=user)
        serializer = self.serializer_class(bookmark, many=True)
        return Response(serializer.data)

    def post(self, request, *args, **kwargs):
        request.data['user'] = request.user.id
        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

