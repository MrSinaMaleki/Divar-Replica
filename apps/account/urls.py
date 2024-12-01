from django.urls import path
from apps.account import views
urlpatterns = [
    path('login/', views.SignRegister.as_view(), name='login'),
    path('verify/', views.Verify.as_view(), name='verify'),
    path('api/token/refresh/', views.TokenRefreshView.as_view(), name='token_refresh'),
]
