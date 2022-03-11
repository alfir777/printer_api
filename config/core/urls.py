from django.urls import path, include
from drf_yasg import openapi
from drf_yasg.generators import OpenAPISchemaGenerator
from drf_yasg.views import get_schema_view
from rest_framework import permissions

from core.api import NewChecks, CheckPDF, CreateChecks


class CustomOpenAPISchemaGenerator(OpenAPISchemaGenerator):
    def get_schema(self, request=None, public=False):
        swagger = super().get_schema(request, public)
        swagger.tags = [
            {
                "name": "erp",
                "description": "Методы API для ERP"
            },
            {
                "name": "app",
                "description": "Методы API для приложения"
            },
        ]
        return swagger


schema_view = get_schema_view(
    openapi.Info(
        title='Printer API',
        default_version='1.0.0',
        description='API для сервиса печати чеков',
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
    generator_class=CustomOpenAPISchemaGenerator,
)

urlpatterns = [
    path('', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('django-rq/', include('django_rq.urls')),
    path('create_checks/', CreateChecks.as_view()),
    path('new_checks/', NewChecks.as_view()),
    path('check/', CheckPDF.as_view()),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]
