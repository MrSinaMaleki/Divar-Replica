from django.core.management.base import BaseCommand
from apps.category.models import Category

categories_data = {
    "categories": {
        "املاک": {
            "image": "https://example.com/images/real-estate.jpg",
            "subcategories": {
                "آپارتمان": ["فروش", "اجاره"],
                "خانه و ویلا": ["فروش", "اجاره"],
                "زمین و کلنگی": ["فروش"],
                "اداری و تجاری": ["فروش", "اجاره"],
                "مغازه": ["فروش", "اجاره"]
            }
        },
        "وسایل نقلیه": {
            "image": "https://example.com/images/vehicles.jpg",
            "subcategories": {
                "خودرو": ["سواری و وانت", "کلاسیک", "اجاره‌ای", "سنگین"],
                "موتورسیکلت": [],
                "قطعات یدکی و لوازم جانبی": [],
                "قایق و وسایل نقلیه دیگر": []
            }
        },
        "کالای دیجیتال": {
            "image": "https://example.com/images/electronics.jpg",
            "subcategories": {
                "گوشی موبایل": ["هوشمند", "معمولی"],
                "رایانه و لپ‌تاپ": ["گیمینگ", "اداری"],
                "دوربین": [],
                "کنسول بازی": [],
                "سایر": []
            }
        },
        "خانه و آشپزخانه": {
            "image": "https://example.com/images/home-kitchen.jpg",
            "subcategories": {
                "لوازم خانگی": ["آشپزخانه", "نظافت"],
                "دکوراسیون": ["مبلمان", "پرده"],
                "ابزار و تجهیزات": ["برقی", "دستی"]
            }
        },
        "شخصی و تفریحی": {
            "image": "https://example.com/images/personal-goods.jpg",
            "subcategories": {
                "پوشاک": ["مردانه", "زنانه", "بچه‌گانه"],
                "زیورآلات": [],
                "سرگرمی و ورزش": ["بازی", "وسایل ورزشی"]
            }
        },
        "خدمات": {
            "image": "https://example.com/images/services.jpg",
            "subcategories": {
                "آرایش و زیبایی": [],
                "تعمیرات": ["خودرو", "خانگی"],
                "آموزشی": ["موسیقی", "زبان"],
                "حمل‌ونقل": []
            }
        },
        "مشاغل و صنعت": {
            "image": "https://example.com/images/jobs.jpg",
            "subcategories": {
                "استخدام": ["تمام‌وقت", "پاره‌وقت"],
                "لوازم صنعتی": [],
                "ابزار": []
            }
        }
    }
}



class Command(BaseCommand):
    help = "Populate or update the category section with main categories, subcategories, and sub-subcategories."

    def handle(self, *args, **kwargs):

        for main_category_title, main_category_data in categories_data["categories"].items():

            main_category, main_created = Category.objects.get_or_create(
                title=main_category_title,
                level=1,
                parent=None
            )
            if main_created:
                self.stdout.write(f"Created main category: {main_category_title}")
            else:
                self.stdout.write(f"Skipped existing main category: {main_category_title}")

            if not main_category.image or main_category.image != main_category_data.get("image"):
                main_category.image = main_category_data.get("image")
                main_category.save()
                self.stdout.write(f"  Updated image for main category: {main_category_title}")

            for subcategory_title, sub_subcategories in main_category_data["subcategories"].items():
                subcategory, sub_created = Category.objects.get_or_create(
                    title=subcategory_title,
                    level=2,
                    parent=main_category
                )
                if sub_created:
                    self.stdout.write(f"  Created subcategory: {subcategory_title}")
                else:
                    self.stdout.write(f"  Skipped existing subcategory: {subcategory_title}")

                for sub_subcategory_title in sub_subcategories:
                    sub_subcategory, sub_sub_created = Category.objects.get_or_create(
                        title=sub_subcategory_title,
                        level=3,
                        parent=subcategory
                    )
                    if sub_sub_created:
                        self.stdout.write(f"    Created sub-subcategory: {sub_subcategory_title}")
                    else:
                        self.stdout.write(f"    Skipped existing sub-subcategory: {sub_subcategory_title}")

        self.stdout.write("Category population and update process completed successfully!")
