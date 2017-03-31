from django.shortcuts import render
from .models import *
from django.db.models import Q
from datetime import date
from datetime import timedelta
from .forms import NewForm, ChartForm
from .script import fun
from django.http import HttpResponse
from graphos.sources.simple import SimpleDataSource
from graphos.renderers.gchart import LineChart
from graphos.renderers import gchart
from graphos.sources.model import ModelDataSource

def formcharts(request):
	form_class = ChartForm()
	return render(request, 'chartForm.html', {'form':form_class})

def charts(request):
	form_class = ChartForm()
	lockerId = request.POST.get('locker_id')
	lockerType = request.POST.get('prime_or_standard')
	if lockerType.lower() == "prime":
		locker_type="Prime"
		locker = Orders.objects.filter(
	    	Q(locker_id=lockerId),Q(order_type=1)
	    ).distinct()
	else:
		locker_type="Standard"
		locker = Orders.objects.filter(
	    	Q(locker_id=lockerId),Q(order_type=2)
	    ).distinct()

	data_source = ModelDataSource(locker,fields=['order_date', 'locker_used'])
	chart = gchart.LineChart(data_source, html_id='gchart_div', options={'title': 'Locker Booking Trends'})
	context = {
		'chart': chart,
		'len':len(locker),
		'locker_id':lockerId,
		'type':locker_type
		}
	return render(request, 'charts.html', context)

def dashboard(request):
	form_class = NewForm

	if request.method == 'POST':
		form = form_class(data=request.POST)

		if form.is_valid():
			q1 = request.POST.get('locker_name')
			q2 = request.POST.get('city')
			q3 = request.POST.get('state')
			q4 = request.POST.get('pincode')
			use_date = form.cleaned_data['user_date']

			date_now = date.today()
			date_1 = date_now + timedelta(days=1)
			date_2 = date_now + timedelta(days=2)
			date_3 = date_now + timedelta(days=3)
			date_4 = date_now + timedelta(days=4)
			date_5 = date_now + timedelta(days=5)

			d={}
			if q1 != "":
				d['locker_name__iexact']=q1;
			if q2 != "":
				d['city__iexact']=q2;
			if q3 != "":
				d['state__iexact']=q3;
			if q4 != "":
				d['pincode__iexact']=q4;

			obj = Table1.objects.filter(**d).distinct()
			obj2 = list()
			obj3 = list()
			var = 0
			if use_date > date_5:
				var = 6
			elif use_date==date_now:
				var = 0
			elif use_date==date_1:
				var = 1
			elif use_date==date_2:
				var = 2
			elif use_date==date_3:
				var = 3
			elif use_date==date_4:
				var = 4
			elif use_date==date_5:
				var = 5

			for ob in obj:
				for row in ob.prime_set.all():
					if (var==3) | (var==4) | (var==5) | (var==6):
						obj2.append(ob.prime_capacity)
					elif var==0:
						obj2.append(row.day0)
					elif var==1:
						obj2.append(row.day1)
					elif var==2:
						obj2.append(row.day2)
				for r in ob.standard_set.all():
					if var==6:
						obj3.append(ob.standard_capacity)
					elif var==0:
						obj3.append(r.day0)
					elif var==1:
						obj3.append(r.day1)
					elif var==2:
						obj3.append(r.day2)
					elif var==3:
						obj3.append(r.day3)
					elif var==4:
						obj3.append(r.day4)
					elif var==5:
						obj3.append(r.day5)

			ob = zip(obj, obj2, obj3)
			context = {
			"ob":ob,
			"len":len(obj)
			}
			return render(request, 'dashboard.html', context)
	return render(request, 'dashboard.html', {'form':form_class})

def rotate_day():
    fun()
    return HttpResponse('dashboard.html')