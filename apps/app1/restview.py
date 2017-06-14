from rest_framework.views import APIView
from rest_framework.exceptions import ParseError
from rest_framework.response import Response
from rest_framework import status
from .models import *
from django.db.models import Q


# import requests

class SearchView(APIView):
    def post(self, request, format=None):
        try:
            data = request.data
        except ParseError as error:
            return Response(
                'Invalid JSON - {0}'.format(error.detail),
                status=status.HTTP_400_BAD_REQUEST
            )
        qry = ""
        emps_list = []
        jobs_list = []
        qry=str(request.data['query'])
        if len(qry)>0:
            emps = Employee.objects.filter(Q(name__icontains=qry) | Q(role__contains=qry))
            for emp in emps:
                emps_list.append({'name': emp.name,'role':emp.role,'age':emp.age,'company':emp.company.name})
            jobs= JobOpening.objects.filter(role_name__icontains=qry)

            for job in jobs:
                jobs_list.append({'role_name':job.role_name,'company':job.associated_company.name})





        return Response({'detail': 'POST answer', 'employees': emps_list,'jobs':jobs_list})
