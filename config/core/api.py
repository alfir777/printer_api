import os

from django.core.exceptions import ObjectDoesNotExist
from django.http import JsonResponse, HttpResponse
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.status import HTTP_201_CREATED
from rest_framework.views import APIView

from .models import Check, Printer
from .serializers import ChecksSerializer


class Erp(GenericAPIView):
    serializer_class = ChecksSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        serializer = ChecksSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=HTTP_201_CREATED)
        if serializer.errors['printer_id']:
            response = {
                'error': 'Не существует принтера с таким ID'}
        return JsonResponse(response, status=400)


class App(APIView):
    """Методы API для приложения"""

    def get(self, request, api_key):
        """Список доступных чеков для печати"""
        try:
            if not os.environ['API_KEY_TASKS'] == api_key:
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


class App_pdf(APIView):
    """Методы API для приложения"""

    def get(self, request, check_id, api_key):
        """PDF-файл чека"""
        try:
            printer = Printer.objects.get(api_key=api_key)
        except ObjectDoesNotExist:
            response = {
                'error': 'Ошибка авторизации'
            }
            return JsonResponse(response, status=401)
        try:
            check = Check.objects.get(pk=check_id)
            serializer = ChecksSerializer(check, many=False)
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
        return response
