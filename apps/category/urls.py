from django.urls import path
from apps.category import views


urlpatterns = [
    path('all_categories/', views.CategoryList.as_view(), name='category_list'),
    path('main_categories/', views.MainCategoriesList.as_view(), name='category_list'),


    path('all_fields/', views.FieldsList.as_view(), name='field_list'),

    path('all_category_fields/', views.AllCategoryFilesList.as_view(), name='category_files_list'),
    path('categories/<int:category_id>/fields/', views.CategoryFieldsView.as_view(), name='category-fields'),

    path('<int:category_id>/children/', views.CategoryChildrenView.as_view(), name='category-children'),
]
