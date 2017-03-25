from django import forms #django already has a class called forms

from .models import Table1
from django.contrib.auth.models import User

class PostForm(forms.ModelForm):
    Prime_percentage=forms.CharField()
    class Meta:
        model = Table1 #will follow the Post Model
        fields = ('locker_id','locker_name','city','state','pincode','prime_capacity','standard_capacity','Prime_percentage')

class UserForm(forms.ModelForm):
    password=forms.CharField(widget=forms.PasswordInput)
    class Meta:
        model=User
        fields=['username','email','password']
