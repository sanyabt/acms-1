from django.shortcuts import render
from .models import Table1,Prime,Standard
from django.db.models import Q
from .forms import ItemForm,SearchForm
from itertools import chain

def results(request):
	form = SearchForm()
	quantity=request.GET.get("quantity")	
	query = request.GET.get("search")
	qlist = Prime.objects.all().select_related('locker').values('locker__locker_name','locker__city','locker__locker_id', 'locker__state','locker__pincode','day2').distinct().order_by('locker__locker_name')
	qlist1 = Standard.objects.all().select_related('locker').values('locker__locker_name','locker__city','locker__locker_id', 'locker__state','locker__pincode','day5').distinct().order_by('locker__locker_name')
	if query:
		qlist = qlist.filter(Q(locker__city=query)|Q(locker__state__icontains=query)|Q(locker__pincode__icontains=query)).order_by('locker__locker_name')
		qlist1 = qlist1.filter(Q(locker__city=query)|Q(locker__state__icontains=query)|Q(locker__pincode__icontains=query)).order_by('locker__locker_name')
		mylist = zip(qlist, qlist1)
	return render(request, 'lock/results.html', {'query':query,'mylist':mylist,'quantity':quantity,'form': form,})

def item(request):
    form = ItemForm()
    return render(request,'lock/items.html', {'form': form})

def success(request,quantity="1", name="1"):
	q1 = request.GET.get("chooseone")
	quantity=int(quantity)
	if q1=="Prime":
		obj=Prime.objects.get(locker=name)
		if obj.day2>=quantity:
			obj.day2=obj.day2-quantity
			obj.save()
	elif q1=="Standard":
		obj=Standard.objects.get(locker=name)
		if obj.day5>=quantity:
			obj.day5=obj.day5-quantity
			obj.save()
	obj=Table1.objects.get(locker_id=name)
	address = obj.city+", "+ obj.state + "-" + obj.pincode
	name = obj.locker_name	
	return render(request, 'lock/success.html',{'quantity':quantity,'name': name,'address':address})
'''	q1 = request.GET.get("chooseone")
	q3 = request.GET.get('lockerName')	
	if q1 == 'yes':
       		if p.prime > 0:
            		p.prime = p.prime - quantity
        	elif q2 == 'yes':
        		if p.standard > 0:
            		p.standard = p.standard - quantity
        post.save()
'''