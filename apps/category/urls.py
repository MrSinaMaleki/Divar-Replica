from django.urls import path
from apps.category import views


urlpatterns = [
    path('all_categories/', views.CategoryList.as_view(), name='category_list'),


]
