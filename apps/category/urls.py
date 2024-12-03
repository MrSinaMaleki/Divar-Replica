from django.urls import path
from apps.category import views


urlpatterns = [
    path('', views.CategoryList.as_view(), name='category_list'),

]
