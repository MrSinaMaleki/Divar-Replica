from apps.post.models import Post
from rest_framework import generics
from rest_framework.permissions import AllowAny
from .serializers import PostSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from apps.category.serializers import FieldSerializer
from apps.category.models import Category
from rest_framework import status
from apps.category.models import PostField
from apps.post.models import PostImage, Post

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
