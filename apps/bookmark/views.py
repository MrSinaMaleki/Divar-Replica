from django.shortcuts import render
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status
from rest_framework.generics import ListCreateAPIView
from apps.bookmark.serializer import FavoriteAddSerializer
from apps.bookmark.models import Bookmark

class FavoriteAddView(ListCreateAPIView):
    serializer_class = FavoriteAddSerializer
    queryset = Bookmark.objects.all()
