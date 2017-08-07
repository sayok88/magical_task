
from django.contrib.auth.forms import AuthenticationForm
from django import forms
from django.forms import ModelForm
from .models import *
from django.db.models import Q
class LoginForm(AuthenticationForm):
    """Login form."""

    username = forms.CharField(
        label="Username",
        max_length=30,
        widget=forms.TextInput(
            attrs={'class': 'mdl-textfield__input', 'name': 'username'}))
    password = forms.CharField(
        label="Password",
        max_length=30,
        widget=forms.PasswordInput(
            attrs={'class': 'mdl-textfield__input', 'name': 'password'}))
class EmployeeForm(ModelForm):
    class Meta:
        model=Employee
        fields=['name','role','age']
class JobForm(ModelForm):
    class Meta:
        model=JobOpening
        fields=['role_name']
class RegistrationForm(forms.Form):
    username = forms.CharField(label="",widget=forms.TextInput(attrs={'placeholder': 'Username','class':'form-control input-perso'}),max_length=30,min_length=3)
    first_name= forms.CharField(label="", widget=forms.TextInput(
        attrs={'placeholder': 'First Name', 'class': 'form-control input-perso'}), max_length=30, min_length=3)
    last_name = forms.CharField(label="", widget=forms.TextInput(
        attrs={'placeholder': 'Last Name', 'class': 'form-control input-perso'}), max_length=30, min_length=3)
    company=forms.CharField(label="", widget=forms.TextInput(
        attrs={'placeholder': 'Company', 'class': 'form-control input-perso'}), max_length=30, min_length=3)
    email = forms.EmailField(label="",widget=forms.EmailInput(attrs={'placeholder': 'Email','class':'form-control input-perso'}),max_length=100,error_messages={'invalid': ("Email invalide.")})
    password1 = forms.CharField(label="",max_length=50,min_length=6,
                                widget=forms.PasswordInput(attrs={'placeholder': 'Password','class':'form-control input-perso'}))
    password2 = forms.CharField(label="",max_length=50,min_length=6,
                                widget=forms.PasswordInput(attrs={'placeholder': 'Confirm password','class':'form-control input-perso'}))


    #recaptcha = ReCaptchaField()

    #Override of clean method for password check
    def clean(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')

        if password1 and password1 != password2:
            self._errors['password2'] = [u"Password don't match!"]

        return self.cleaned_data

    #Override of save method for saving both User and companuser objects
    def save(self, datas):
        u = User.objects.create_user(datas['username'],
                                     datas['email'],
                                     datas['password1'])
        u.is_active = True
        u.first_name=datas['first_name']
        u.last_name = datas['last_name']
        comp=datas['company']
        comps = Company.objects.filter(Q(name__icontains=comp) )
        if comps:
            comps=comps.first()
        else:
            comps=Company(name=comp,total_employees=0,location=Location.objects.first())
            comps.save()

        u.save()
        compuser=CompanyUser(user=u,company=comps)
        compuser.save()

        return u

