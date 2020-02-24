from django.db import models

# Create your models here.

class Bike(models.Model):
    bikeObj = models.Manager()
    bikeid = models.CharField(max_length=20)
    bikelocation = models.CharField(max_length=20)
    statement = models.BooleanField(default=False)
    bikeprice = models.FloatField()
    isused = models.BooleanField(default=False)
    def _str_(self):
        return self.bikeid
    class Meta:
        db_table = "bike"
        ordering = ['id']

class Costumer(models.Model):
    costumerObj = models.Manager()
    userid = models.CharField(max_length=20)
    username = models.CharField(max_length=20)
    userpassword = models.CharField(max_length=20)
    telephone = models.IntegerField()
    userlocation = models.CharField(max_length=20,null=True)
    balance = models.FloatField(null=True)
    renttime = models.DateTimeField(null=True)
    returntime = models.DateTimeField(null=True)
    authority = models.CharField(max_length=20,null=True)
    def _str_(self):
        return self.username
    class Meta:
        db_table = "costumer"
        ordering = ['id']

class Operator(models.Model):
    operatorObj = models.Manager()
    opid = models.CharField(max_length=20)
    opname = models.CharField(max_length=20)
    oppassword = models.CharField(max_length=20)
    authority = models.CharField(max_length=20,null=True)
    def _str_(self):
        return self.opname
    class Meta:
        db_table = "operator"
        ordering = ['id']

class Manager(models.Model):
    manageObj = models.Manager()
    manid = models.CharField(max_length=20)
    manname = models.CharField(max_length=20)
    manpassword = models.CharField(max_length=20)
    authority = models.CharField(max_length=20,null=True)
    def _str_(self):
        return self.manname
    class Meta:
        db_table = "manager"
        ordering = ['id']