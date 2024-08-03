from django.db import models
from django_jalali.db import models as jmodels

class BarTime(models.Model):

    name = models.CharField(max_length=200)
    datetime = jmodels.jDateTimeField(auto_now_add=True)

    def __str__(self):
        return "%s, %s" % (self.name, self.datetime)