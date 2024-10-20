from django.db import models
from account.models import *

class Meeting(models.Model):
    title = models.CharField(max_length=255, verbose_name='عنوان جلسه')
    meeting_date = models.DateTimeField(verbose_name='تاریخ جلسه')
    description = models.TextField(blank=True, null=True, verbose_name='توضیحات جلسه')
    participants = models.ManyToManyField(User, related_name='meetings', verbose_name='شرکت‌کنندگان')
    records = models.TextField(blank=True, null=True, verbose_name='صورت جلسه')

    def __str__(self):
        return self.title
