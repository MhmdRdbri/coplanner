# project/tasks.py

from celery import shared_task
from django.utils import timezone
from datetime import timedelta
from .models import Project
import http.client
import json

@shared_task
def check_project_end_dates():
    now = timezone.now().date()
    one_week_later = now + timedelta(days=7)

    projects = Project.objects.filter(
        models.Q(host_end_date=one_week_later) | models.Q(domain_end_date=one_week_later)
    )

    for project in projects:
        if project.responsible_person:
            conn = http.client.HTTPSConnection("api2.ippanel.com")
            payload = json.dumps({
                "code": "b8d9tqdjn0qxf1w",
                "sender": "+983000505",
                "recipient": project.responsible_person.phone_number,
                "variable": {
                    "full_name": f"{project.responsible_person.full_name}",
                }
            })
            headers = {
                'apikey': ' SZtX_MYwI2E0jWqdkrSoDV3-02u0yF-l2c1LXgZVZpw= ',
                'Content-Type': 'application/json'
            }
            conn.request("POST", "/api/v1/sms/pattern/normal/send", payload, headers)
            res = conn.getresponse()
            data = res.read()
            print(data.decode("utf-8"))