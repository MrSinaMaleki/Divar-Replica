from django.urls import path
from apps.category.views import CategoryChildrenView
from django.views.generic import TemplateView

urlpatterns = [
    path('create/', TemplateView.as_view(template_name='posts/add_posts.html'), name='add_posts'),

]
