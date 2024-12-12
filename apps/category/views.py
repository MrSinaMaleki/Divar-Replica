from rest_framework.permissions import AllowAny
from rest_framework.generics import ListAPIView

from apps.category.serializers import CategorySerializer, FieldSerializer, FieldCategorySerializer
from apps.category.models import Category, Field
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status

# redis cash decorator inserter.

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

class MainCategoriesList(ListAPIView):
    """
         - example response

                {
                    "id": 1,
                    "title": "main category",
                    "level": 1,
                    "image": "src link",
                    "parent": null
                }


    """
    permission_classes = (AllowAny,)
    queryset = Category.objects.filter(level=1).order_by('id')
    serializer_class = CategorySerializer


class FieldsList(ListAPIView):
    """
        - example request

            {
                "category": 3,
                "name": "field name",
                "is_optional": false or true,
                "f_type": "int-str-dropdown",
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

       """

    permission_classes = (AllowAny,)
    queryset = Field.objects.all().order_by('id')
    serializer_class = FieldSerializer


class AllCategoryFilesList(ListAPIView):
    """
             - example response

                {
                        "id": 3,
                        "title": "موبایل ایفون",
                        "fields": [
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
                        ],
                        "parent": 2
                }


    """
    permission_classes = (AllowAny,)
    queryset = Category.objects.all().order_by('id')
    serializer_class = FieldCategorySerializer


class CategoryChildrenView(APIView):
    """
    {
        "id": 3,
        "title": "آیفون",
        "level": 3,
        "image": null,
        "parent": 2
    }
    """
    permission_classes = (AllowAny,)
    def get(self, request, category_id):
        try:
            category = Category.objects.get(id=category_id)
        except Category.DoesNotExist:
            return Response({'detail': 'Category not found'}, status=status.HTTP_404_NOT_FOUND)

        sub_cats = Category.objects.filter(parent=category)
        serializer = CategorySerializer(sub_cats, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class CategoryFieldsView(APIView):
    """
     - example response

                {
                        "id": 3,
                        "title": "موبایل ایفون",
                        "fields": [
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
                        ],
                        "parent": 2
                }


    """
    permission_classes = [AllowAny,]
    def get(self, request, category_id):
        try:
            category = Category.objects.get(id=category_id)
        except Category.DoesNotExist:
            return Response({'detail': 'Category not found'}, status=status.HTTP_404_NOT_FOUND)


        serializer = FieldCategorySerializer(category)
        return Response(serializer.data, status=status.HTTP_200_OK)

