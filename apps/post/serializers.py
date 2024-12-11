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
    image = serializers.ImageField()
    caption = serializers.CharField(required=False, allow_blank=True)
    is_cover = serializers.BooleanField()

    class Meta:
        model = PostImage
        fields = ['image', 'caption', 'is_cover']

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



class PostFieldSerializer(serializers.ModelSerializer):
    field_id = serializers.IntegerField()

    class Meta:
        model = PostField
        fields = ['field_id', 'value']


class AddPostSerializer(serializers.ModelSerializer):
    category_id = serializers.IntegerField()
    user_id = serializers.IntegerField()
    location_id = serializers.IntegerField()
    fields = PostFieldSerializer(many=True, required=False)

    class Meta:
        model = Post
        fields = [
            'title', 'description', 'laddered', 'category_id', 'user_id',
            'location_id', 'video', 'fields'
        ]

    def validate(self, data):
        # Validate category
        category = Category.objects.filter(id=data['category_id'], level=3).first()
        if not category:
            raise serializers.ValidationError("Category must be a level-3 category.")

        # Validate user
        if not User.objects.filter(id=data['user_id']).exists():
            raise serializers.ValidationError("Invalid user ID.")

        # Validate location
        if not Location.objects.filter(id=data['location_id'], type=2).exists():
            raise serializers.ValidationError("Invalid location ID.")

        # Validate fields
        required_fields = Field.objects.filter(category_id=data['category_id'], is_optional=False)
        provided_field_ids = {field['field_id'] for field in data.get('fields', [])}

        missing_fields = [
            field.name for field in required_fields if field.id not in provided_field_ids
        ]
        if missing_fields:
            raise serializers.ValidationError(f"Missing required fields: {', '.join(missing_fields)}")

        return data

    def create(self, validated_data):
        # Extract fields and images data
        fields_data = validated_data.pop('fields', [])
        category = Category.objects.get(id=validated_data['category_id'])
        user = User.objects.get(id=validated_data['user_id'])
        location = Location.objects.get(id=validated_data['location_id'])

        # Create the post
        post = Post.objects.create(
            title=validated_data['title'],
            description=validated_data['description'],
            laddered=validated_data['laddered'],
            category=category,
            user=user,
            location=location,
            video=validated_data.get('video'),
        )

        # Create PostFields
        for field_data in fields_data:
            field = Field.objects.get(id=field_data['field_id'])
            PostField.objects.create(post=post, field=field, value=field_data['value'])

        return post