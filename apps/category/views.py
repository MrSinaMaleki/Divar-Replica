from pip._vendor.requests.models import Response
from rest_framework.permissions import AllowAny
from rest_framework.generics import ListAPIView

from apps.category.serializers import CategorySerializer
from apps.category.models import Category
from rest_framework.response import Response


# Create your views here.
class CategoryList(ListAPIView):
    permission_classes = (AllowAny,)
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = (AllowAny,)

