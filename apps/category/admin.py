from django.contrib import admin

from apps.category.models import Category, Field

# Register your models here.

class CategoryAdmin(admin.ModelAdmin):
    def get_model_perms(self, request):
        if request.user.role == 'god':
            return super().get_model_perms(request)
        return {}

admin.site.register(Category, CategoryAdmin)


class FieldAdmin(admin.ModelAdmin):
    def get_model_perms(self, request):
        if request.user.role == 'god':
            return super().get_model_perms(request)
        return {}

admin.site.register(Field, FieldAdmin)
