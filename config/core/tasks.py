import os
from datetime import datetime

import requests

from .services import get_html_to_pdf


def new_checks():
    url = f"http://{os.environ['IP_SERVER']}:{os.environ['IP_SERVER_PORT']}/new_checks/{os.environ['API_KEY_TASKS']}/"
    headers = {
        'Content-Type': 'application/json',
    }
    response = requests.get(url, headers=headers).json()
    for i in response:
        get_html_to_pdf(i['id'])


def streams_tasks(scheduler):
    scheduler.schedule(
        scheduled_time=datetime.utcnow(),
        func=new_checks,
        interval=10,
    )
