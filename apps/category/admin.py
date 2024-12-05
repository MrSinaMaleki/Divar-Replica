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

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'category':
            kwargs['queryset'] = Category.objects.filter(level=3)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


admin.site.register(Field, FieldAdmin)
