from __future__ import unicode_literals

from django.db import models

# Create your models here.


class User(models.Model):
    userName = models.CharField(unique=True, max_length=250)
    password = models.CharField(max_length=250)
    email = models.EmailField()
    mobile = models.CharField(max_length=15)

    def __str__(self):
        return self.userName + "  ,  " + self.password + "  ,  " + self.mobile + " , "+self.email
