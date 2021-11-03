from django.core.exceptions import ObjectDoesNotExist
from django.http import JsonResponse, HttpResponse
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import BasePermission, SAFE_METHODS
from rest_framework.response import Response
from rest_framework.status import HTTP_201_CREATED
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet

from .models import Check, Printer
from .serializers import ChecksSerializer


class ReadOnly(BasePermission):
    def has_permission(self, request, view):
        return request.method in SAFE_METHODS


class ReadOnlyApiKey(BasePermission):
    def has_permission(self, request, view):
        if request.method == 'DELETE':
            return False
        return request.method in SAFE_METHODS


class CheckViewSet(ModelViewSet):
    """API для сервиса печати чеков"""
    queryset = Check.objects.all()
    serializer_class = ChecksSerializer


class Erp(GenericAPIView):
    serializer_class = ChecksSerializer

    def post(self, request, *args, **kwargs):
        serializer = ChecksSerializer(data=request.data)
        print(request.data['type'])
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=HTTP_201_CREATED)
        response = {
            'error': 'Ошибка авторизации'
        }
        if serializer.errors['printer_id']:
            response = {
                'error': 'Ошибка авторизации'}
        return JsonResponse(response, status=400)


class App(APIView):
    """Методы API для приложения"""

    def get(self, request, api_key):
        """Список доступных чеков для печати"""
        try:
            printer = Printer.objects.get(api_key=api_key)
        except ObjectDoesNotExist:
            response = {
                'error': 'Ошибка авторизации'
            }
            return JsonResponse(response, status=401)
        try:
            queryset = Check.objects.filter(status='new')
            serializer = ChecksSerializer(queryset, many=True)
            return Response(serializer.data)
        except ObjectDoesNotExist:
            response = {
                'info': 'Все чеки распечатаны'
            }
            return JsonResponse(response)
        response = {
            'error': 'Исключительный случай'
        }
        return JsonResponse(response)


class App_pdf(APIView):
    """Методы API для приложения"""

    def get(self, request, check_id, api_key):
        """Список доступных чеков для печати"""
        try:
            printer = Printer.objects.get(api_key=api_key)
        except ObjectDoesNotExist:
            response = {
                'error': 'Ошибка авторизации'
            }
            return JsonResponse(response, status=401)
        try:
            check = Check.objects.get(pk=check_id)
            print(type(check.pdf_file))

            serializer = ChecksSerializer(check, many=False)
            try:
                with open(check.pdf_file.path, 'rb') as file:
                    response = HttpResponse(file, content_type='application/pdf')
            except ValueError:
                response = {
                    'error': 'Для данного чека не сгенерирован PDF-файл'
                }
                return JsonResponse(response, status=400)
            return response
        except ObjectDoesNotExist:
            response = {
                'info': 'Данного чека не существует'
            }
            return JsonResponse(response, status=400)
        response = {
            'error': 'Исключительный случай'
        }
        return JsonResponse(response)
