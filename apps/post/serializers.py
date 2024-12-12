from rest_framework import serializers

from apps.category.models import Field, Category,PostField
from apps.core.models import Location
from apps.post.models import Post, PostImage
from django.contrib.auth import get_user_model
from apps.account.serializers import  UserSerializer
User = get_user_model()


class FieldSerializer(serializers.ModelSerializer):
    class Meta:
        model = Field
        fields = ['id', 'name', 'is_optional']


class PostImagesSerializer(serializers.ModelSerializer):
    post = serializers.PrimaryKeyRelatedField(queryset=Post.objects.all())
    class Meta:
        model = PostImage
        fields = ['image', 'caption', 'is_cover', 'post']

    def create(self, validated_data):
        return super().create(validated_data)


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
        category_id = data.get('category_id')
        if not category_id:
            raise serializers.ValidationError("Category ID is missing.")

        required_fields = Field.objects.filter(category_id=category_id, is_optional=False)
        provided_fields = {str(field.get('field_id')): field.get('value') for field in data.get('fields', [])}

        missing_fields = [
            field.name
            for field in required_fields
            if str(field.id) not in provided_fields or not provided_fields[str(field.id)]
        ]

        if missing_fields:
            raise serializers.ValidationError(
                {"fields": f"Missing or empty required fields: {', '.join(missing_fields)}"}
            )

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


class AllPostsSerializer(serializers.ModelSerializer):
    images = PostImagesSerializer(many=True, read_only=True)

    class Meta:
        model = Post
        fields = [
            'id',
            'title',
            'description',
            'laddered',
            'user',
            'location',
            'created_at',
            'images',

        ]

class PostDetailSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())
    images = PostImagesSerializer(many=True, read_only=True)
    fields = PostFieldSerializer(many=True, read_only=True)
    category = CategorySerializer(read_only=True)

    class Meta:
        model = Post
        fields = [
            'id',
            'title',
            'description',
            'laddered',
            'category',
            'user',
            'location',
            'created_at',
            'video',
            'images',
            'fields',
        ]


class PostOwnerDetailSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    class Meta:
        model = Post
        fields = ['id','user']

