from django.core.exceptions import ObjectDoesNotExist
from django.http import JsonResponse
from django.shortcuts import render

from .models import Printer, Check
from .services import get_html_to_pdf


def index(request):
    """
    Функция для проверки работы другой функции get_html_to_pdf
    """
    data = request.GET
    try:
        printer = Printer.objects.get(api_key=data['api_key'])
    except ObjectDoesNotExist:
        response = {
            'error': 'Ошибка авторизации'
        }
        return JsonResponse(response, status=401)

    check = Check.objects.get(pk=9)

    context = {
        'check': check,
    }
    get_html_to_pdf(9)
    return render(request, 'kitchen_check.html', context=context)
