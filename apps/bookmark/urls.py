from django.urls import path
from apps.bookmark.views import FavoriteAddView

urlpatterns = [
    path('bookmarks/', FavoriteAddView.as_view(), name='-'),

]
