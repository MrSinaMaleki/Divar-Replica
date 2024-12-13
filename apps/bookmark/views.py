from django.shortcuts import render
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from apps.bookmark.serializer import BookMarkSerializer
from apps.bookmark.models import Bookmark

# Create your views here.
# class BookMarkCreateListView(APIView):
#     serializer_class = BookMarkSerializer
#     """
#     Viewing and adding more post
#     """
#     def get(self, request, *args, **kwargs):
#         user = request.user
#         bookmark = Bookmark.objects.filter(user=user,)
#         serializer = self.serializer_class(bookmark, many=True)
#         return Response(serializer.data)
#
#     def post(self, request, *args, **kwargs):
#         data = request.data.copy()
#         data['user'] = request.user.id
#         # print("user: ",data['user'])
#         # print("data", data)
#         serializer = self.serializer_class(data=data)
#
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#
#     def patch(self, request, *args, **kwargs):
#         # print("request data: ",request.data)
#         try:
#             bookmark = Bookmark.objects.get(id=request.id, user=request.user)
#         except Bookmark.DoesNotExist:
#             return Response({"detail": "Bookmark not found"},
#                             status=status.HTTP_404_NOT_FOUND)
#
#         data = request.data.copy()
#         serializer = self.serializer_class(bookmark, data=data, partial=True)
#
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_200_OK)
#
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
