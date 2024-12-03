from django.contrib import admin

from apps.account.models import User


# Register your models here.
class UserAdmin(admin.ModelAdmin):
    list_display = ('email', 'role', 'nationality', 'is_dad')
    list_filter = ('is_dad', )

admin.site.register(User, UserAdmin)
