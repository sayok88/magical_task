# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib.admin import models
from django.db import models
from django.contrib.auth.models import User


class Location(models.Model):
    name=models.CharField(max_length=100)
    def __str__(self):  # __unicode__ on Python 2
        return self.name
# Create your models here.
class Company(models.Model):
    name=models.CharField(max_length=100)
    total_employees=models.IntegerField(default=0)
    location=models.ForeignKey(Location)
    def __str__(self):  # __unicode__ on Python 2
        return self.name

class Employee(models.Model):
    name=models.CharField(max_length=100)
    role=models.CharField(max_length=50)
    age=models.IntegerField()
    company=models.ForeignKey(Company)
    __original_company=None

    def __str__(self):  # __unicode__ on Python 2
        return self.name
    def __init__(self, *args, **kwargs):
        super(Employee, self).__init__(*args, **kwargs)
        try:
            self.__original_company = self.company
        except:
            pass

    def save(self,force_insert=False, force_update=False,* args, ** kwargs):
        if self.__original_company is None:
            super(Employee,self).save(force_insert,force_update * args, ** kwargs)
            self.company.total_employees+=1
            self.company.save()
        else:
            if self.company != self.__original_company:
                self.__original_company.total_employees-=1
                self.__original_company.save()
                super(Employee, self).save(force_insert,force_update * args, ** kwargs)
                self.company.total_employees += 1
                self.company.save()
        self.__original_company = self.company
    # Wont work if used from admin panel
    def delete(self,* args, ** kwargs):
        self.company.total_employees -= 1
        self.company.save()
        super(Employee,self).delete(* args, ** kwargs)
class JobOpening(models.Model):
    role_name=models.CharField(max_length=50)
    associated_company=models.ForeignKey(Company)
class CompanyUser(models.Model):
    user=models.ForeignKey(User)
    company=models.ForeignKey(Company,null=True)
    def __str__(self):
        return self.user.username+' '+self.company.name
# Roles can be further normalized but additional information regardings roles are
# company specific or not is not provided hence it is not undertaken
