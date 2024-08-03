from django.db import models
from account.models import CustomUser
from django_jalali.db import models as jmodels
import http.client
import json


class SMSLog(models.Model):
    project = models.ForeignKey('Project', on_delete=models.CASCADE, related_name='sms_logs')
    full_name = models.CharField(max_length=150)
    result = models.TextField()
    status = models.CharField(max_length=20, choices=(
        ('sent', 'Sent'),
        ('error', 'Error'),
        ('none', 'None')
    ))
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.full_name} - {self.status}"


class Project(models.Model):
    name = models.CharField(max_length=150)
    full_name = models.CharField(max_length=150)
    phone_number = models.CharField(max_length=15)
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
    
    domain = models.CharField(max_length=255, null=True, blank=True)
    design_files = models.FileField(upload_to='design_files/', null=True, blank=True)
    domain_start_date = models.DateField(null=True, blank=True)
    domain_end_date = models.DateField(null=True, blank=True)
    host_start_date = models.DateField(null=True, blank=True)
    host_end_date = models.DateField(null=True, blank=True)
    TEAM_CHOICES = [
        ('wordpress', 'Wordpress'),
        ('technical', 'Technical'),
        ('seo', 'SEO'),
        ('digital_marketing', 'Digital Marketing'),
        # Add more teams as needed
    ]
    team = models.CharField(max_length=50, choices=TEAM_CHOICES, null=True, blank=True)
    design_team_members = models.ManyToManyField(CustomUser, related_name='design_projects', blank=True)
    deploy_team_members = models.ManyToManyField(CustomUser, related_name='deploy_projects', blank=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if self.pk is None:
            super().save(*args, **kwargs)
            if self.responsible_person:
                conn = http.client.HTTPSConnection("api2.ippanel.com")
                payload = json.dumps({
                    "code": "grsavr8kfgqazyn",
                    "sender": "+983000505",
                    "recipient": self.phone_number,
                    "variable": {
                        "full_name": f"{self.full_name}",
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