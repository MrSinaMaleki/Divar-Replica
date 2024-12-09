from django.urls import path
from apps.category.views import CategoryChildrenView
from django.views.generic import TemplateView
from apps.post.views import PostFieldsAPIView

urlpatterns = [
    path('create/', TemplateView.as_view(template_name='posts/add_posts.html'), name='add_posts'),
    path('post-fields/<int:category_id>/', PostFieldsAPIView.as_view(), name='post-fields'),
    path('post-fields/', PostFieldsAPIView.as_view(), name='post-create'),
]
