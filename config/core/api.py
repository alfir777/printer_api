import django_rq
from django.core.exceptions import ObjectDoesNotExist
from django.http import JsonResponse, HttpResponse
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework.decorators import action
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Check, Printer
from .serializers import ChecksSerializer, CreateChecksSerializer
from .tasks import get_html_to_pdf

RESPONSE_SCHEMA_DICT = {
    "200": openapi.Response(
        description="Чеки успешно созданы",
        examples={
            "application/json": {
                "ok": "Чеки успешно созданы"
            }
        },
    ),
    "400": openapi.Response(
        description='При создании чеков произошла одна из ошибок:\n'
                    '1. Для данного заказа уже созданы чеки\n'
                    '2. Для данной точки не настроено ни одного принтера\n',
        examples={
            "application/json": {
                "error": "string"
            }
        },
    ),
}


class CreateChecks(CreateAPIView):
    serializer_class = CreateChecksSerializer
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        methods=['POST', ],
        responses=RESPONSE_SCHEMA_DICT,
        operation_summary='Создание чеков для заказа',
        tags=['erp', ],
    )
    @action(detail=False, methods=['POST', ])
    def post(self, request, *args, **kwargs):
        serializer = CreateChecksSerializer(data=request.data)
        if serializer.is_valid():
            try:
                serializer.save()
                data = serializer.data
                django_rq.enqueue(get_html_to_pdf, data)
                response = {
                    'ok': 'Чеки успешно созданы'
                }
                return JsonResponse(response, status=201)
            except ValueError:
                response = {
                    'error': 'string'
                }
                return JsonResponse(response, status=400)


class NewChecks(APIView):

    @swagger_auto_schema(
        methods=['GET', ],
        manual_parameters=[
            openapi.Parameter('api_key', openapi.IN_QUERY, description="Ключ доступа к API", type=openapi.TYPE_STRING,
                              required=True)
        ],
        operation_summary='Список доступных чеков для печати',
        tags=['app', ],
    )
    @action(detail=False, methods=['GET', ])
    def get(self, request):
        api_key = request.query_params.get('api_key')
        try:
            Printer.objects.get(api_key=api_key)
        except ObjectDoesNotExist:
            response = {
                'error': 'Ошибка авторизации'
            }
            return JsonResponse(response, status=401)
        try:
            queryset = Check.objects.filter(status='new')
            serializer = ChecksSerializer(queryset, many=True)
            return Response({'checks': serializer.data})
        except ObjectDoesNotExist:
            response = {
                'info': 'Все чеки распечатаны'
            }
            return JsonResponse(response)


class CheckPDF(APIView):

    @swagger_auto_schema(
        methods=['GET', ],
        manual_parameters=[
            openapi.Parameter('api_key', openapi.IN_QUERY, description="Ключ доступа к API", type=openapi.TYPE_STRING,
                              required=True),
            openapi.Parameter('check_id', openapi.IN_QUERY, description="ID чека", type=openapi.TYPE_INTEGER,
                              required=True)
        ],
        operation_summary='PDF-файл чека',
        tags=['app', ]
    )
    @action(detail=False, methods=['GET', ])
    def get(self, request):
        api_key = request.query_params.get('api_key')
        check_id = request.query_params.get('check_id')
        try:
            Printer.objects.get(api_key=api_key)
        except ObjectDoesNotExist:
            response = {
                'error': 'Ошибка авторизации'
            }
            return JsonResponse(response, status=401)
        try:
            check = Check.objects.get(pk=check_id)
        except ObjectDoesNotExist:
            response = {
                'info': 'Данного чека не существует'
            }
            return JsonResponse(response, status=400)
        try:
            with open(check.pdf_file.path, 'rb') as file:
                response = HttpResponse(file, content_type='application/pdf')
        except ValueError:
            response = {
                'error': 'Для данного чека не сгенерирован PDF-файл'
            }
            return JsonResponse(response, status=400)
        except FileNotFoundError:
            response = {
                'error': 'Для данного чека PDF-файл сформирован, но недоступен'
            }
            return JsonResponse(response, status=400)
        return HttpResponse(response, status=200)
