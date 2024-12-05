from django.urls import path
from apps.post import views
from .views import PostCreateView, get_category_fields

urlpatterns = [
    path('all_posts', views.PostList.as_view(), name='PostList'),
    path('category/<int:category_id>/fields/', get_category_fields, name='get_category_fields'),
    path('post/create/', PostCreateView.as_view(), name='create_post'),

]