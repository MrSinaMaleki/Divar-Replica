from rest_framework.generics import RetrieveAPIView

from apps.post.models import Post
from rest_framework import generics
from rest_framework.permissions import AllowAny
from .serializers import PostSerializer,PostDetailSerializer, AllPostsSerializer,AddPostSerializer, PostImagesSerializer, PostOwnerDetailSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from apps.category.serializers import FieldSerializer
from apps.category.models import Category
from rest_framework import status
from apps.post.models import PostImage
from apps.category.models import PostField
from apps.post.models import PostImage, Post
from django.shortcuts import get_object_or_404
from apps.post.serializers import PostLaddered
from django.core.cache import cache
from apps.core.models import Location
from django.db.models import Q
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page

class PostFieldsAPIView(APIView):
    """
             - example response

                    {
                        "post_fields": [
                            "title",
                            "description",
                            "laddered",
                            "category",
                            "user",
                            "location",
                            "fields",
                            "images"
                        ],
                        "category_fields": [
                            {
                                "category": 3,
                                "name": "درصد باتری",
                                "is_optional": false,
                                "f_type": "int",
                                "drop_down_menu_options": null,
                                "id": 1
                            },
                            {
                                "category": 3,
                                "name": "رنگ",
                                "is_optional": true,
                                "f_type": "str",
                                "drop_down_menu_options": null,
                                "id": 2
                            }
                        ]
                    }

    """

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
    """
                 - example response

                       {
                            "title": "",
                            "description": "",
                            "laddered": false,
                            "category_id": null,
                            "user_id": null,
                            "location_id": null,
                            "video": null,
                            "fields": []
                       }

    """


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
    """
                     - example response

                          {
                            "id": 1,
                            "title": "Iphone 16",
                            "description": "تست توضیحات :)",
                            "laddered": false,
                            "user": 1,
                            "location": 77,
                            "created_at": "2024-12-11T14:34:16.349094+03:30",
                            "images": []
                          },

    """
    permission_classes = (AllowAny,)
    serializer_class = AllPostsSerializer
    queryset = Post.objects.filter(status="accepted", is_delete=False)


class PostDetails(RetrieveAPIView):
    """
        - example response

            {
                "id": 7,
                "title": "iphone",
                "description": "w[dkwd",
                "laddered": false,
                "category": {
                    "id": 3,
                    "title": "موبایل ایفون",
                    "level": 3,
                    "fields": [
                        {
                            "id": 1,
                            "name": "درصد باتری",
                            "is_optional": false
                        },
                        {
                            "id": 2,
                            "name": "رنگ",
                            "is_optional": true
                        }
                    ]
                },
                "user": 1,
                "location": 46,
                "created_at": "2024-12-11T23:40:35.895583+03:30",
                "video": null,
                "images": [
                    {
                        "image": "http://localhost:8000/storage/media/images/2024/12/11/car_it3TRNa.png",
                        "caption": "iphone",
                        "is_cover": true,
                        "post": 7
                    },
                    {
                        "image": "http://localhost:8000/storage/media/images/2024/12/11/MainAfter_3Cip7Z7.jpg",
                        "caption": "iphone",
                        "is_cover": false,
                        "post": 7
                    }
                ]
            }
    """
    queryset = Post.objects.all()
    serializer_class = PostDetailSerializer
    permission_classes = [AllowAny, ]

    def get_object(self):
        post_id = self.kwargs.get('id')
        return get_object_or_404(Post, id=post_id)

    # def list(self, request, *args, **kwargs):
    #     print("lists has been called. ")
    #     cache_key = "all_posts"
    #     cached_data = cache.get(cache_key)
    #     if cached_data:
    #         print("Cache hit!")  # Log cache hit
    #     else:
    #         print("Cache miss!")  # Log cache miss
    #
    #     return super().list(request, *args, **kwargs)


class PostOwnerDetails(RetrieveAPIView):
    """
            - example response

                {
                    "id": 7,
                    "user": {
                        "id": 1,
                        "username": null,
                        "email": "s@gmail.com",
                        "first_name": "",
                        "last_name": ""
                    }
                }

    """
    queryset = Post.objects.all()
    serializer_class = PostOwnerDetailSerializer


    def get_object(self):
        post_id = self.kwargs.get('id')
        return get_object_or_404(Post, id=post_id)


class PostLadder(APIView):
    serializer_class = PostLaddered

    def post(self, request, *args, **kwargs):
        post_id = request.data.get('post_id')
        if not post_id:
            return Response({"error": "Post ID is required."}, status=status.HTTP_400_BAD_REQUEST)

        post = get_object_or_404(Post, id=post_id)

        if post.user != request.user and not request.user.is_staff:
            return Response(
                {"error": "You do not have permission to ladder this post."},
                status=status.HTTP_403_FORBIDDEN
            )

        post.laddered = True
        post.save()

        # Return a success response
        return Response({"message": "Post laddred successfully."}, status=status.HTTP_200_OK)


class PostSearchView(APIView):
    serializer_class = AllPostsSerializer
    permission_classes = (AllowAny, )
    def get(self, request, *args, **kwargs):
        cache_key = f"posts_search_{request.query_params.urlencode()}"
        cached_posts = cache.get(cache_key)

        if cached_posts:
            return Response(cached_posts, status=status.HTTP_200_OK)

        posts = Post.objects.filter(status="accepted", is_delete='False')
        title = request.query_params.get('title', None)
        category = request.query_params.get('category', None)
        location = request.query_params.get('location', None)

        if title:
            posts = posts.filter(title__icontains=title)
        if category:
            try:
                selected_category = Category.objects.get(id=category)

                if selected_category.level == 1:
                    level2_ids = Category.objects.filter(parent=selected_category).values_list('id', flat=True)
                    level3_ids = Category.objects.filter(parent__in=level2_ids).values_list('id', flat=True)
                    posts = posts.filter(
                        Q(category_id=category) | Q(category_id__in=level2_ids) | Q(category_id__in=level3_ids))

                elif selected_category.level == 2:
                    level3_ids = Category.objects.filter(parent=selected_category).values_list('id', flat=True)
                    posts = posts.filter(Q(category_id=category) | Q(category_id__in=level3_ids))

                elif selected_category.level == 3:
                    posts = posts.filter(category_id=category)

            except Category.DoesNotExist:
                posts = posts.none()

        if location:
            try:
                selected_location = Location.objects.get(id=location)
                if selected_location.type == 1:
                    child_area_ids = selected_location.sub_areas.filter(type=2).values_list('id', flat=True)
                    posts = posts.filter(Q(location_id=location) | Q(location_id__in=child_area_ids))
                else:
                    posts = posts.filter(location_id=location)

            except Location.DoesNotExist:
                posts = posts.none()

        serializer = self.serializer_class(posts, many=True)

        cache.set(cache_key, serializer.data, 60 * 5)
        return Response(serializer.data, status=status.HTTP_200_OK)

