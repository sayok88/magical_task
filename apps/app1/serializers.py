from rest_framework import serializers
from .models import *


class CompanySerializer(serializers.HyperlinkedModelSerializer):
    location_name=serializers.CharField(source='location.name')
    class Meta:
        model= Company
        fields= ('name','total_employees','location_name')

class LocationSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model= Location
        fields= ('name',)

class EmployeeSerializer(serializers.ModelSerializer):
    company_name = serializers.CharField(source='company.name')
    class Meta:
        model= Employee
        fields= ('name','role','age','company_name')
