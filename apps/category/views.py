from rest_framework.permissions import AllowAny
from rest_framework.generics import ListAPIView

from apps.category.serializers import CategorySerializer
from apps.category.models import Category
from rest_framework.response import Response


class CategoryList(ListAPIView):
    """
         - example response

                {
                "id": 1,
                "title": "Main Category",
                "level": 1,
                "image": "Some URL",
                "parent": null
                },
                {
                  "id": 2,
                  "title": "Sub Category",
                  "level": 2,
                  "image": null,
                  "parent": 1
                },
                {
                  "id": 3,
                  "title": "Sub-Sub Category",
                  "level": 3,
                  "image": null,
                  "parent": 2
                },


    """

    permission_classes = (AllowAny,)
    queryset = Category.objects.all().order_by('id')
    serializer_class = CategorySerializer
    ordering_fields = ['id', 'title']
    ordering = ['id']

