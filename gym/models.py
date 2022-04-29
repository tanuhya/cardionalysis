from django.db import models

# Create your models here.
from django.db.models import CharField


class Enquiry(models.Model):
    name = models.CharField(max_length=100)
    contact = models.IntegerField()
    emailid = models.CharField(max_length=50)
    age = models.IntegerField()
    gender = models.CharField(max_length=10)

    def __str__(self):
        return self.name


class Equipment(models.Model):
    name = models.CharField(max_length=100)
    price = models.IntegerField()
    unit = models.IntegerField()
    date = models.DateField()
    description = models.CharField(max_length=200)

    def __str__(self):
        return self.name


class Plan(models.Model):
    name = models.CharField(max_length=50)
    amount = models.IntegerField()
    duration = models.CharField(max_length=10)

    def __str__(self):
        return self.name


class Member(models.Model):
    name = models.CharField(max_length=50)
    contact = models.CharField(max_length=10)
    emailid = models.CharField(max_length=50)
    age = models.CharField(max_length=10)
    gender = models.CharField(max_length=10)
    plan = models.CharField(max_length=40)
    joindate = models.CharField(max_length=40)
    expiredate = models.CharField(max_length=40)
    initialamount = models.IntegerField()

    def __str__(self):
        return self.name

class Attendance(models.Model):
    name = models.CharField(max_length=50)
    date=models.CharField(max_length=40,unique=True)
    status = models.CharField(max_length=10)

    class Meta:
        unique_together = ["date", "name"]

    def __str__(self):
        return self.name