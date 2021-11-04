from datetime import datetime

import requests

from .services import get_html_to_pdf


def new_checks():
    url = 'http://127.0.0.1:8000/new_checks/123/'
    headers = {
        'Content-Type': 'application/json',
    }
    response = requests.get(url, headers=headers).json()
    for i in response:
        get_html_to_pdf(i['id'])


def streams_tasks(scheduler):
    scheduler.schedule(
        scheduled_time=datetime.utcnow(),
        func=get_html_to_pdf,
        interval=10,
    )
