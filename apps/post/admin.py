from django.contrib import admin

from apps.post.models import Post


# Register your models here.
class PostAdmin(admin.ModelAdmin):
    list_display = ('status', 'title', 'description', 'laddered', 'category', 'user', 'location', 'created_at')
    list_filter = ('status', )

admin.site.register(Post, PostAdmin)

