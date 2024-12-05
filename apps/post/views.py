from apps.post.models import Post
from apps.post.serializers import PostSerializer
from rest_framework import generics
from rest_framework.permissions import AllowAny
from rest_framework.response import Response


# Create your views here.
class PostList(generics.ListCreateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [AllowAny]

    def list(self, request):
        # Note the use of `get_queryset()` instead of `self.queryset`
        queryset = self.get_queryset()
        serializer = PostSerializer(queryset, many=True)
        return Response(serializer.data)


from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Category
from .serializers import CategorySerializer, PostSerializer

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from apps.category.models import Category
from apps.category.serializers import CategorySerializer

class CategoryFieldsView(APIView):
    permission_classes = [AllowAny]
    def get(self, request, category_id, *args, **kwargs):
        try:
            category = Category.objects.get(id=category_id)
        except Category.DoesNotExist:
            return Response({'detail': 'Category not found'}, status=status.HTTP_404_NOT_FOUND)

        # Serialize category data along with associated fields
        serializer = CategorySerializer(category)
        return Response(serializer.data, status=status.HTTP_200_OK)



class PostCreateView(APIView):
    permission_classes = [AllowAny]
    def post(self, request, *args, **kwargs):
        serializer = PostSerializer(data=request.data)
        if serializer.is_valid():
            # Create a new post and save user input for fields
            post = serializer.save()
            return Response(PostSerializer(post).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
