from django.db import models
from account.models import CustomUser
from django_jalali.db import models as jmodels
import http.client
import json

class Project(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    start_date = models.DateField()
    end_date = models.DateField()
    status = models.CharField(max_length=20, choices=(
        ('not_started', 'Not Started'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed')
    ))
    priority = models.CharField(max_length=20, choices=(
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High')
    ))
    responsible_person = models.ForeignKey(CustomUser, related_name='responsible_projects', on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if self.pk is None:
            super().save(*args, **kwargs)
            if self.responsible_person:
                conn = http.client.HTTPSConnection("api2.ippanel.com")
                payload = json.dumps({
                "code": "b8d9tqdjn0qxf1w",
                "sender": "+983000505",
                "recipient": self.responsible_person.phone_number,
                "variable": {
                    "full_name": f"{self.responsible_person.full_name}",
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
        else:
            super().save(*args, **kwargs)