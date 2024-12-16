from django.urls import path
from apps.bookmark.views import FavoriteAddView
from apps.bookmark.views import MyLikedPosts
from django.views.generic import TemplateView

urlpatterns = [
    path('bookmarks/', FavoriteAddView.as_view(), name='-'),
    path('api/my_liked_posts', MyLikedPosts.as_view(), name='my_liked_posts_api'),
    path('my_liked_posts', TemplateView.as_view(template_name='profile/my_liked_posts.html'), name='my_liked_posts'),
]
