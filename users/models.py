from __future__ import unicode_literals

from django.db import models


from django.utils import timezone

# Create your models here.


class User(models.Model):
    userName = models.CharField(primary_key=True, unique=True, max_length=250)
    password = models.CharField(max_length=250)
    email = models.EmailField()
    mobile = models.CharField(max_length=15)

    def __str__(self):
        return self.userName + "  ,  " + self.password + "  ,  " + self.mobile + " , "+self.email

"""
class Finding(models.Model):
    findingId = models.AutoField(primary_key=True)
    userName = models.ForeignKey('userName.User')
    dateTime = models.DateTimeField(default=timezone.now())
    status = models.BooleanField(default=False)


class Missing(models.Model):
    missingId = models.AutoField(primary_key=True)
    userName = models.ForeignKey('userName.User')
    dateTime = models.DateTimeField(default=timezone.now())
    status = models.BooleanField(default=False)
"""