from django.urls import path, include
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions
from rest_framework.routers import SimpleRouter

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
    path('', include(router.urls)),
    path('django-rq/', include('django_rq.urls')),
    path('index', index),
    path('new_checks/<api_key>/', App.as_view()),
    path('check/<check_id>/<api_key>/', App_pdf.as_view()),
    path('create_checks/', Erp.as_view()),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]
