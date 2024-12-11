from apps.post.models import Post
from rest_framework import generics
from rest_framework.permissions import AllowAny
from .serializers import PostSerializer, AllPostsSerializer,AddPostSerializer, PostImagesSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from apps.category.serializers import FieldSerializer
from apps.category.models import Category
from rest_framework import status
from apps.post.models import PostImage
from apps.category.models import PostField
from apps.post.models import PostImage, Post
from rest_framework.parsers import MultiPartParser, FormParser

class PostFieldsAPIView(APIView):
    permission_classes = (AllowAny,)
    def get(self, request, category_id):
        try:

            category = Category.objects.prefetch_related('fields').get(id=category_id)
            # print("category fields",category.fields.all())


            category_fields_serializer = FieldSerializer(category.fields.all(), many=True)

            # Get the default post fields
            post_serializer = PostSerializer()
            post_fields = [field for field in post_serializer.get_fields()]
            # print("def post fields: ", post_fields)


            response_data = {
                'post_fields': post_fields,
                'category_fields': category_fields_serializer.data,
            }

            return Response(response_data, status=status.HTTP_200_OK)
        except Category.DoesNotExist:
            return Response({"error": "Category not found"}, status=status.HTTP_404_NOT_FOUND)


class PostCreateAPIView(generics.CreateAPIView):
    serializer_class = AddPostSerializer
    def post(self, request, *args, **kwargs):
        print(request.data)
        serializer = AddPostSerializer(data=request.data)
        if serializer.is_valid():
            post = serializer.save()
            return Response({"message": "Post created successfully.", "post_id": post.id}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AddImagesAPIView(APIView):
    serializer_class = PostImagesSerializer

    def post(self, request, *args, **kwargs):
        post_id = request.data.get('post_id')
        images = request.data.getlist('images')
        captions = request.data.getlist('caption')
        is_cover_list = request.data.getlist('is_cover')

        if len(images) != len(captions) or len(captions) != len(is_cover_list):
            return Response({"error": "Mismatch between number of images, captions, and cover statuses."},
                            status=status.HTTP_400_BAD_REQUEST)

        image_data = []
        for index, image in enumerate(images):
            image_data.append({
                'image': image,
                'caption': captions[index] if captions[index] != 'null' else '',
                'is_cover': is_cover_list[index] == 'true',
                'post': post_id,
            })

        serializer = PostImagesSerializer(data=image_data, many=True)

        if serializer.is_valid():
            post_images = serializer.save()
            return Response({"message": "Images were added successfully."}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class AllPosts(generics.ListAPIView):
    permission_classes = (AllowAny,)
    serializer_class = AllPostsSerializer
    queryset = Post.objects.all()


