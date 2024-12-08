from django.contrib import admin

from apps.account.models import User


# Register your models here.
class UserAdmin(admin.ModelAdmin):
    list_display = ('email', 'role', 'nationality', 'is_verified')
    list_filter = ('is_verified', )

admin.site.register(User, UserAdmin)
