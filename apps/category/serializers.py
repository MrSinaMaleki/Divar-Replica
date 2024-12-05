from rest_framework import serializers
from apps.category.models import Category
from apps.category.models import Field

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'title', 'level', 'image', 'parent']


class FieldSerializer(serializers.ModelSerializer):
    class Meta:
        model = Field
        fields = ['category', 'name', 'is_optional']
