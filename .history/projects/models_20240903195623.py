from django.db import models
from account.models import CustomUser
from django_jalali.db import models as jmodels
import http.client
import json
from telegram import Bot
from django.conf import settings  # Ensure you have your settings configured properly
import logging
import asyncio
from django.core.exceptions import ValidationError
import os


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
    project_name = models.CharField(max_length=150)
    manager_full_name = models.CharField(max_length=150)
    phone_number = models.CharField(max_length=15)
    description = models.TextField()
    start_date = models.DateField()
    end_date = models.DateField()
    status = models.CharField(max_length=20, choices=(
        ('not_started', 'Not Started'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed')
    ))
    responsible_person = models.ForeignKey(CustomUser, related_name='responsible_projects', on_delete=models.SET_NULL, null=True, blank=True)
    team_members = models.ManyToManyField(CustomUser, related_name='projects', blank=True)
    domain = models.CharField(max_length=255, null=True, blank=True)
    design_files = models.FileField(upload_to='design_files/', null=True, blank=True)
    domain_end_date = models.DateField(null=True, blank=True)
    host_end_date = models.DateField(null=True, blank=True)
    contract_files = models.FileField(upload_to='contract_files/',null=True, blank=True)

    def __str__(self):
        return self.project_name

        
    def clean(self):
        for field in ['design_files', 'contract_files']:
            file = getattr(self, field)
            if file:
                ext = os.path.splitext(file.name)[1].lower()
                if ext != '.zip':
                    raise ValidationError(f"{field.replace('_', ' ').capitalize()} must be a .zip file.")


    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if self.responsible_person :
            status = 'none'
            result = ''
            try:

                chat_id = self.responsible_person.telegram_chat_id
                bot_token = '7052281105:AAG5x1yux4ryfDzvfAmn1mwuVqa4LmBtKkk'
                bot = Bot(token=bot_token)
                message = f" پروژه تازه ای به نام '{self.project_name}' برای شما ایجاد شده است"
                
                logging.debug(f"Attempting to send message to chat_id: {chat_id}")

                asyncio.run(bot.send_message(chat_id=chat_id, text=message))
                logging.info(f"Sent message to {chat_id}: {message}")


            except Exception as e:
                logging.error(f"Failed to send Telegram message: {e}")




        #         conn = http.client.HTTPSConnection("api2.ippanel.com")
        #         payload = json.dumps({
        #             "code": "grsavr8kfgqazyn",
        #             "sender": "+983000505",
        #             "recipient": self.phone_number,
        #             "variable": {
        #                 "full_name": f"{self.full_name}",
        #             }
        #         })
        #         headers = {
        #             'apikey': ' SZtX_MYwI2E0jWqdkrSoDV3-02u0yF-l2c1LXgZVZpw= ',
        #             'Content-Type': 'application/json'
        #         }
        #         conn.request("POST", "/api/v1/sms/pattern/normal/send", payload, headers)
        #         res = conn.getresponse()
        #         result = res.read().decode("utf-8")
        #         if res.status == 200:
        #             status = 'sent'
        #         else:
        #             status = 'error'
        #     except Exception as e:
        #         result = str(e)
        #         status = 'error'

        #     SMSLog.objects.create(
        #         project=self,
        #         full_name=self.full_name,
        #         result=result,
        #         status=status
        #     )