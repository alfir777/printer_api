"""config URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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
from rest_framework.routers import SimpleRouter
from rest_framework import permissions
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from django.conf import settings
from django.conf.urls.static import static

from core.api import App, App_pdf, Erp, CheckViewSet
from core.views import index

schema_view = get_schema_view(
    openapi.Info(
        title='Printer API',
        default_version='1.0.0',
        description='API для сервиса печати чеков',
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

router = SimpleRouter()

router.register('create', CheckViewSet)

urlpatterns = [
    path('', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('index', index),
    path('', include(router.urls)),
    path('admin/', admin.site.urls),
    path('new_checks/<api_key>/', App.as_view()),
    path('check/<check_id>/<api_key>/', App_pdf.as_view()),
    path('create_checks/', Erp.as_view()),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
