"""
URL configuration for config project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include

from apps import account
from config import settings
from django.conf.urls.static import static
from drf_spectacular.views import SpectacularAPIView, SpectacularRedocView, SpectacularSwaggerView
from django.views.generic import TemplateView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('account/', include('apps.account.urls')),

    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    # Optional UI:
    path('api/swagger-api/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('api/schema/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),

    path('temp/', TemplateView.as_view(template_name='temp.html'), name='temp'),

    path('category/', include('apps.category.urls'), name='category'),
]

if settings.DEBUG:
    urlpatterns += (static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) +
                    static(settings.STATIC_URL, document_root=settings.STATIC_ROOT_custom))
