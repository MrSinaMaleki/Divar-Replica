from rest_framework import serializers
from apps.bookmark.models import Bookmark

class BookMarkSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bookmark
        fields = ['user', 'posts', 'notes', 'id']

