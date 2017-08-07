# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib.auth import authenticate, login,logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from rest_framework import viewsets
from .models import *
from  .serializers import *
from django.shortcuts import render
from .forms import *

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
def logout1(request):
    logout(request)

    return HttpResponseRedirect('/')
def elogin(request):
    errmsg = ""
    next = ""
    uid = 0
    resendemail = False
    if request.GET:
        next = request.GET['next']
        #print(next)
        request.session['next'] = next
    if request.method == 'POST':
        form2 = LoginForm(request.POST)
        print(request.POST)
        print(form2)
        next = request.session.get('next', {})
        print(len(next))
        username = request.POST['username']
        password = request.POST['password']
        print(username)
        user2 = None
        try:
            user2 = User.objects.get(username=username)
        except:
            print('no user, should exit here')
        user = authenticate(username=username, password=password)
        if user is None and user2 is not None:
            user = authenticate(username=user2.email, password=password)
        if user is not None:

            login(request, user)

            if len(next) > 0:
                return HttpResponseRedirect(next)
            return HttpResponseRedirect("/")
        else:
            errmsg = "Error in username and password combination"
    form1 = LoginForm()
    return render(request, "login.html", {'form': form1, 'errmsg': errmsg})

def register(request):
    if request.user.is_authenticated():
        return HttpResponseRedirect(home)
    registration_form = RegistrationForm()
    if request.method == 'POST':
        form = RegistrationForm(request.POST)

        if form.is_valid():
            datas={}
            datas['username']=form.cleaned_data['username']
            datas['email']=form.cleaned_data['email']
            datas['password1']=form.cleaned_data['password1']

            datas['first_name']= form.cleaned_data['first_name']
            datas['last_name']= form.cleaned_data['last_name']
            datas['company']= form.cleaned_data['company']

            u=form.save(datas) #Save the user and his profile
            login(request,u)


            return HttpResponseRedirect('/')
        else:
            registration_form = form #Display form with error messages (incorrect fields, etc)

    return render(request, 'register.html', {'form': registration_form})
@login_required
def addemployee(request):
    form=None
    if request.method=='POST':
        form=EmployeeForm(request.POST)
        emp=form.save(commit=False)
        emp.company=CompanyUser.objects.filter(user=request.user).first().company
        emp.save()
        return HttpResponseRedirect('/addemployee')

    else:
        form=EmployeeForm()
    return render(request,"add_employee.html",{'form':form})
@login_required
def addjob(request):
    form=None
    if request.method=='POST':
        form=JobForm(request.POST)
        job=form.save(commit=False)
        job.associated_company=CompanyUser.objects.filter(user=request.user).first().company
        job.save()
        return HttpResponseRedirect('/addjob')

    else:
        form=JobForm()
    return render(request,"add_job.html",{'form':form})
