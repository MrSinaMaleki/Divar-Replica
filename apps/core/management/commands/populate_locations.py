import requests
from django.core.management.base import BaseCommand
from django.db import IntegrityError
from apps.core.models import Location
import sys
import io

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')


# bulk create (bug fix)
class Command(BaseCommand):
    help = 'Populate provinces and areas from the Iran locations API'

    def handle(self, *args, **kwargs):
        provinces_url = 'https://iran-locations-api.ir/api/v1/fa/states'
        provinces_response = requests.get(provinces_url)

        if provinces_response.status_code == 200:
            provinces_data = provinces_response.json()
            for province in provinces_data:

                province_obj, created = Location.objects.get_or_create(
                    title=province['name'],
                    type=1,
                )
                if created:
                    self.stdout.write(f"Saved province: {province_obj.title}")
                else:
                    self.stdout.write(f"Province already exists: {province_obj.title}")


                areas_url = f'https://iran-locations-api.ir/api/v1/fa/cities?state_id={province["id"]}'
                areas_response = requests.get(areas_url)

                if areas_response.status_code == 200:
                    areas_data = areas_response.json()
                    for area in areas_data:

                        existing_area = Location.objects.filter(
                            title=area['name'],
                            type=2,
                            parent=province_obj,
                        ).first()

                        if existing_area:
                            self.stdout.write(f"Area already exists under {province_obj.title}: {existing_area.title}")
                        else:
                            try:
                                area_obj = Location.objects.create(
                                    title=area['name'],
                                    type=2,
                                    parent=province_obj,
                                )
                                self.stdout.write(f"Saved area: {area_obj.title}")
                            except IntegrityError:
                                self.stdout.write(f"Failed to save area (integrity error): {area['name']}")
                else:
                    self.stdout.write(f"Failed to fetch areas for province: {province['name']}")
        else:
            self.stdout.write("Failed to fetch provinces")
