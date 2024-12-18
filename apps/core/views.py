from rest_framework.permissions import AllowAny
from rest_framework.generics import ListAPIView

from apps.core.serializers import LocationSerializer
from apps.core.models import Location
from rest_framework.response import Response
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page

@method_decorator(cache_page(60 * 15), name="dispatch")
class LocationList(ListAPIView):
    """
         - example response

                {
                "id": 1,
                "title": "Provice",
                "level": 1,
                "parent": null
                },
                {
                  "id": 2,
                  "title": "Area",
                  "level": 2,
                  "parent": 1
                },


    """

    permission_classes = (AllowAny,)
    queryset = Location.objects.all().order_by('id')
    serializer_class = LocationSerializer
    ordering_fields = ['id', 'title']
    ordering = ['id']

