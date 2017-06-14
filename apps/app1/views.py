# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from rest_framework import viewsets
from .models import *
from  .serializers import *
from django.shortcuts import render

# Create your views here.


class EmployeeViewSet(viewsets.ModelViewSet):

    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer
class CompanyViewSet(viewsets.ModelViewSet):
    queryset = Company.objects.all()
    serializer_class = CompanySerializer
class LocationViewSet(viewsets.ModelViewSet):
    queryset = Location.objects.all()
    serializer_class = LocationSerializer



def home(request):
    return render(request, "search.html" )