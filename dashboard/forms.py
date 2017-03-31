from django import forms
import datetime
from django.forms import ModelForm
from .models import Table1, Prime, Standard

class NewForm(ModelForm):
	user_date = forms.DateField(required=True, label='Enter date (yyyy-mm-dd)', initial=datetime.date.today)
	class Meta:
		model = Table1
		fields = ['locker_name', 'city', 'state', 'pincode']

class ChartForm(forms.Form):
	locker_id = forms.IntegerField(required=True, label='Locker ID')
	prime_or_standard = forms.CharField(required=True, label='Prime/Standard')