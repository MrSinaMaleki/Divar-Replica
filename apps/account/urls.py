from xml.dom.expatbuilder import TEXT_NODE

from django.urls import path
from apps.account import views
from django.views.generic import TemplateView
from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns = [
    path('loginAPI/', views.SignRegister.as_view(), name='login'),
    path('login/', TemplateView.as_view(template_name='account/login.html'), name='login'),

    path('logout/', views.logout_view, name='logout'),
    path('verifyAPI/', views.Verify.as_view(), name='verify'),

    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    path('profile/', TemplateView.as_view(template_name='profile/profile.html'), name='profile'),
    path('api/profile/<int:pk>', views.Profile.as_view(), name='profile_api'),
    path('profile/verifycheck/', TemplateView.as_view(template_name='profile/verify.html'), name='verify_check'),
    path('api/profile/verifycheck/', views.VerifyCheck.as_view(), name='profile/verify'),

]
