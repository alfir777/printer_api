from .models import Check
from .services import wkhtmltopdf


def get_html_to_pdf(data) -> None:
    checks = Check.objects.filter(order=data)
    for check in checks:
        wkhtmltopdf(check)
