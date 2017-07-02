from __future__ import unicode_literals

from django.db import models
from django.core.validators import MaxValueValidator

# Create your models here.


class User(models.Model):
    userName = models.CharField(unique=True, max_length=250)
    password = models.CharField(max_length=250)
    email = models.EmailField()
    mobile = models.CharField(max_length=15)

    def __str__(self):
        return "%s %s" % (self.userName, self.password)
       # return self.userName + "  ,  " + self.password + "  ,  " + self.mobile + " , "+self.email


class FindRequest(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField(null=False)
    fName = models.CharField(max_length=100)
    gender = models.CharField(max_length=1)
    status = models.BooleanField(default=False)
    stop = models.PositiveIntegerField(validators=[MaxValueValidator(9999999999)], default=0)
    type = models.CharField(max_length=1, default='f')

    class Meta:
        unique_together = (('user', 'date'),)

    def __str__(self):
        return "%s %s %s" % (self.user, self.date, self.status)

            #return self.dateTime + " , "+self.status


class MissRequest(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField(null=False)
    fName = models.CharField(max_length=100)
    gender = models.CharField(max_length=1)
    status = models.BooleanField(default=False)
    stop = models.PositiveIntegerField(validators=[MaxValueValidator(9999999999)], default=0)
    type = models.CharField(max_length=1, default='m')

    class Meta:
        unique_together = (('user', 'date'),)

    def __str__(self):
        return "%s %s %s" % (self.user, self.date, self.status)



# table of images in case of find someone
"""

class FaceF(models.Model):
    faceFId = models.AutoField(primary_key=True)
    fIdRequest = models.ForeignKey(FindRequest, on_delete=models.CASCADE, db_column="fIdRequest")
    faceImage = models.FileField()

    def __str__(self):
        return self.faceFId + "  ,  " + self.fIdRequest + "  ,  " + self.faceImage


class MissRequest(models.Model):
    mIdRequest = models.AutoField(primary_key=True)
    userId = models.ForeignKey(User, on_delete=models.CASCADE, db_column="userId", null=True)
    dateTime = models.DateTimeField(default=timezone.now)
    status = models.BooleanField(default=False)

    def __str__(self):
        return self.userId + "  ,  " + self.mIdRequest + "  ,  " + self.userName  + "  ,  " + self.dateTime + " , "+self.status

# table of images in case of search someone


class FaceM(models.Model):
    faceMId = models.AutoField(primary_key=True)
    mIdRequest = models.ForeignKey(MissRequest, on_delete=models.CASCADE, db_column="mIdRequest")
    faceImage = models.FileField()

    def __str__(self):
        return self.faceMId + "  ,  " + self.mIdRequest + "  ,  " + self.faceImage
"""