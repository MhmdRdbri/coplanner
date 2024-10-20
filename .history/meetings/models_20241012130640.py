from django.db import models

class Meeting(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=255, verbose_name='عنوان جلسه')
    meeting_date = models.DateTimeField(verbose_name='تاریخ جلسه')
    description = models.TextField(blank=True, null=True, verbose_name='توضیحات جلسه')
    participants = models.JSONField(verbose_name='شناسه‌های شرکت‌کنندگان')
    minutes = models.TextField(blank=True, null=True, verbose_name='صورت جلسه')

    def __str__(self):
        return self.title
