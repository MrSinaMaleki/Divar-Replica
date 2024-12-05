from django.urls import path
from apps.post import views
from .views import PostCreateView
from .views import CategoryFieldsView

urlpatterns = [
    path('all_posts', views.PostList.as_view(), name='PostList'),
    path('cat/<int:category_id>/fields/', CategoryFieldsView.as_view(), name='get_category_fields'),
    path('create/', PostCreateView.as_view(), name='create_post'),

]