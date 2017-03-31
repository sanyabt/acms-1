from django.shortcuts import render
from .models import Table1,Prime,Standard
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from django.shortcuts import redirect
from django.db.models import Q
from django.conf import settings
from django import http
from .forms import UserForm, PostForm
from django.contrib.auth import authenticate, login
from django.contrib.auth import logout
from django.db import connection


def post_new(request):
    if request.method == "POST":
        form = PostForm(request.POST)    #method name -GET or Post is specified in the dictionary value
        if form.is_valid():
            post = form.save(commit=False)
            post.save()
            lock_id = request.POST.get('locker_id')
            p_cap = request.POST.get('prime_capacity')
            s_cap = request.POST.get('standard_capacity')
            newobj_p = Prime(locker_id=lock_id, day0=p_cap, day1=p_cap, day2=p_cap)
            newobj_s = Standard(locker_id=lock_id, day0=s_cap, day1=s_cap, day2=s_cap, day3=s_cap, day4=s_cap, day5=s_cap)
            newobj_p.save()
            newobj_s.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm()
    return render(request, 'post_add.html', {'form': form})


def post_edit(request, pk):
    post = get_object_or_404(Table1, pk=pk)
    #categories = Category.objects.all
    if request.method == "POST":
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            with connection.cursor() as cursor:
                cursor.execute("SELECT day0,day1,day2 FROM prime WHERE locker_id = %s", [pk])
                row = cursor.fetchall()
                a=row[0][0]
                b=row[0][1]
                c=row[0][2]
                res=min(a,min(b,c))
                cursor.execute("SELECT prime_capacity FROM table1 WHERE locker_id = %s", [pk])
                row = cursor.fetchall()
                prime_cap = int(row[0][0])
                prime_res = prime_cap - res
                cursor.execute("SELECT day0,day1,day2,day3,day4,day5 FROM standard WHERE locker_id = %s", [pk])
                row = cursor.fetchall()
                g=row[0][0]
                h=row[0][1]
                i=row[0][2]
                d=row[0][3]
                e=row[0][4]
                f=row[0][5]
                res=min(g,min(h,min(i,min(d,min(e,f)))))
                cursor.execute("SELECT standard_capacity FROM table1 WHERE locker_id = %s", [pk])
                row = cursor.fetchall()
                standard_cap = int(row[0][0])
                standard_res = standard_cap - res
                total_cap = standard_cap + prime_cap
                prime_percentage = int(form.cleaned_data['Prime_percentage'])
                standard_percentage = 100 - prime_percentage
                prime_cap_new = int((total_cap*prime_percentage)/100)
                standard_cap_new = total_cap - prime_cap_new
                prime_diff = prime_cap_new - prime_cap
                a=a+prime_diff
                b=b+prime_diff
                c=c+prime_diff
                standard_diff = standard_cap_new - standard_cap
                d=d+standard_diff
                e=e+standard_diff
                f=f+standard_diff
                g=g+standard_diff
                h=h+standard_diff
                i=i+standard_diff
                if prime_cap_new >= prime_res and standard_cap_new >= standard_res:
                    cursor.execute("UPDATE prime SET day0 = %s, day1 = %s, day2 = %s WHERE locker_id = %s", [a,b,c,pk])
                    cursor.execute("UPDATE standard SET day0 = %s, day1 = %s, day2 = %s, day3 = %s, day4 = %s, day5 = %s WHERE locker_id = %s", [g,h,i,d,e,f,pk])
                    post = form.save(commit=False)
                    post.prime_capacity = prime_cap_new
                    post.standard_capacity = standard_cap_new
                    post.save()
                    return redirect('post_detail', pk=pk)
                else:
                    return render(request, 'post_edit.html', {'form': form, 'a': 0})            
    else:
        form = PostForm(instance=post)
    return render(request, 'post_edit.html', {'form': form, 'a': 1})


def searchResults(request):
    posts = Table1.objects.all()
    query=request.GET.get("q")
    if query:
        posts = posts.filter(
            Q(city__iexact=query)|
            Q(state__iexact=query)|
            Q(locker_name__icontains=query)|
            Q(pincode__iexact=query)|
            Q(standard_capacity__iexact=query)|
            Q(prime_capacity__iexact=query)|
            Q(locker_id__iexact=query)
            ).distinct()
    return render(request, 'post_list.html', {'posts': posts})


def post_list(request):
    posts = Table1.objects.all()
    return render(request, 'post_list.html', {'posts': posts})


def post_detail(request, pk):  #matches url of type post/2005
    post = get_object_or_404(Table1, pk=pk)
    return render(request, 'post_detail.html', {'post': post})


def post_remove(request, pk):
    post = get_object_or_404(Table1, pk=pk)
    with connection.cursor() as cursor:
        cursor.execute("SELECT day0,day1,day2 FROM prime WHERE locker_id = %s", [pk])
        row = cursor.fetchall()
        a=row[0][0]
        b=row[0][1]
        c=row[0][2]
        cursor.execute("SELECT prime_capacity FROM table1 WHERE locker_id = %s", [pk])
        row = cursor.fetchall()
        prime_cap = int(row[0][0])
        cursor.execute("SELECT day0,day1,day2,day3,day4,day5 FROM standard WHERE locker_id = %s", [pk])
        row = cursor.fetchall()
        g=row[0][0]
        h=row[0][1]
        i=row[0][2]
        d=row[0][3]
        e=row[0][4]
        f=row[0][5]
        res=min(g,min(h,min(i,min(d,min(e,f)))))
        cursor.execute("SELECT standard_capacity FROM table1 WHERE locker_id = %s", [pk])
        row = cursor.fetchall()
        standard_cap = int(row[0][0])
        if a==b and b==c and c==prime_cap and d==e and e==f and f==g and g==h and h==i and i==standard_cap:
            cursor.execute("DELETE FROM standard WHERE locker_id = %s", [pk])
            cursor.execute("DELETE FROM prime WHERE locker_id = %s", [pk])
            post.delete()
            return redirect('post_list')
        else:
            return HttpResponse("ERROR:Can't delete this locker as already occupied")


def login_user(request):
    if request.method == "POST":
        mail = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=mail, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                posts = Table1.objects.all()
                return render(request, 'post_list.html', {'posts': posts})
            else:
                return render(request, 'login.html', {'error_message': 'Your account has been disabled'})
        else:
            return render(request, 'login.html', {'error_message': 'Invalid login'})
    return render(request, 'login.html')


def login_operational_user(request):
    if request.method == "POST":
        mail = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=mail, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                return redirect('/dashboard/')
            else:
                return render(request, 'loginoperational.html', {'error_message': 'Your account has been disabled'})
        else:
            return render(request, 'loginoperational.html', {'error_message': 'Invalid login'})
    return render(request, 'loginoperational.html')


def logout_view(request):
    logout(request)
    return render(request, 'logout.html')


def register(request):
    form = UserForm(request.POST or None)
    if form.is_valid():
        user = form.save(commit=False)
        username = form.cleaned_data['username']
        email = form.cleaned_data['email']
        password = form.cleaned_data['password']
        user.set_password(password)
        user.save()
        user = authenticate(username=username, password=password, email=email)
        if user is not None: 
            if user.is_active:
                #login(request, user)
                q=1
                return render(request,'post_list.html', {'q': q})
        return render(request,'post_list.html', {'q': q})
    context ={
        "form": form,
    }
    return render(request, 'registration_form.html', context)