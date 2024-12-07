from django.urls import path
from apps.category import views


urlpatterns = [
    path('all_categories/', views.CategoryList.as_view(), name='category_list'),
    path('main_categories/', views.MainCategoriesList.as_view(), name='category_list'),


    path('all_fields/', views.FieldsList.as_view(), name='field_list'),

    path('all_category_fields/', views.CategoryFilesList.as_view(), name='category_files_list'),

]
