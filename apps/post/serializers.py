from rest_framework import serializers

from apps.category.models import Field, Category,PostField
from apps.core.models import Location
from apps.post.models import Post, PostImage
from django.contrib.auth import get_user_model
User = get_user_model()


class FieldSerializer(serializers.ModelSerializer):
    class Meta:
        model = Field
        fields = ['id', 'name', 'is_optional', 'value']


class PostImagesSerializer(serializers.ModelSerializer):
    class Meta:
        model = PostImage
        fields = ['id', 'caption', 'is_cover', 'uploaded_at']

class PostSerializer(serializers.ModelSerializer):
    category = serializers.PrimaryKeyRelatedField(queryset=Category.objects.filter(level=3))
    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())
    location = serializers.PrimaryKeyRelatedField(queryset=Location.objects.filter(type=2))
    fields = FieldSerializer(many=True, read_only=True)
    images = PostImagesSerializer(many=True, read_only=True)

    class Meta:
        model = Post
        fields = ['title', 'description', 'laddered','category', 'user', 'location', 'fields', 'images']


    def create(self, validated_data):
        fields_data = validated_data.pop('fields', [])
        post = Post.objects.create(**validated_data)
        for field_data in fields_data:
            field = Field.objects.get(id=field_data['id'])
            PostField.objects.create(post=post, field=field, value=field_data.get('value'))
        return post


class CategorySerializer(serializers.ModelSerializer):
    fields = FieldSerializer(many=True)

    class Meta:
        model = Category
        fields = ['id', 'title', 'level', 'fields']
