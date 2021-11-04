from django.core.files.base import ContentFile
from django.shortcuts import render

import json
import os
import requests
from base64 import b64encode

from .models import Check


def get_html_to_pdf(check_id) -> None:
    url = f"http://{os.environ['WKHTMLTODPF_HOST']}:{os.environ['WKHTMLTODPF_PORT']}/"

    check = Check.objects.get(pk=check_id)
    context = {
        'check': check,
    }

    byte_content = render(None, f'{check.type}_check.html',
                          context=context, content_type='application/json').content

    base64_bytes = b64encode(byte_content)
    base64_string = base64_bytes.decode('utf-8')

    data = {
        'contents': base64_string,
    }
    headers = {
        'Content-Type': 'application/json',
    }

    response = requests.post(url, data=json.dumps(data), headers=headers)

    check.status = 'printed'
    check.pdf_file.save(f'{check.order["id"]}_{check.type}.pdf', ContentFile(response.content))

    check.save()
