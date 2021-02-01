from django.contrib import auth
from django.shortcuts import render,redirect
from django.http import HttpResponse
from .models import employee
from django.contrib.auth.models import User
from .forms import RegisterForm
import datetime
def emp_login_view(request):
    if request.method=='POST':
        username=request.POST.get('username')
        password = request.POST.get('password')
        verify =auth.authenticate(username=username,password=password)
        if verify:
            auth.login(request,verify)
            return redirect(index_view)
        else:
            return HttpResponse('invalid user')
    return render(request,'login.html')
def manager_login_view(request):
    if request.method=='POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        verify = auth.authenticate(username=username,password=password)
        if verify:
            auth.login(request,verify)
            return redirect(manage_dashboard)
        else:
            return HttpResponse('invalid user')
    return render(request,'login.html')
def index_view(request):
    username=request.user.get_username()
    u_data = User.objects.filter(username=username)
    for i in u_data:
        uid = i.id
    start_date = request.POST.get('start_date')
    end_date = request.POST.get('end_date')
    if request.method=='POST':
        data=employee.objects.filter(user_id=uid)
        s_date=None
        for i in data:
            s_date=i.start_date
        if s_date==start_date:
            pass
        else:
            e_data = employee(
                user_id=uid,
                start_date=start_date,
                end_date=end_date,
                r_date=datetime.datetime.now(),
            )
            e_data.save()
    emp_v= employee.objects.filter(status='Pending')
    status=request.GET.get('request')
    if status == 'approved':
        approve_r = employee.objects.filter(status__icontains='approved')
        return render(request, 'index.html', {'approved': approve_r})
    elif status == 'pending':
        pendings = employee.objects.filter(status='Pending')
        return render(request, 'index.html', {'pending': pendings})
    elif status == 'rejected':
        rejects = employee.objects.filter(status__icontains='rejected')
        return render(request, 'index.html', {'rejected': rejects})
    countdata=employee.objects.filter(user_id=uid)
    counts=None
    for i in countdata:
        counts=i.total_v
    return render(request,'index.html',{'pending':emp_v,'count':counts})
def update(request,id):
    status = request.GET.get('request')
    if status=='approved':
        udata=employee.objects.get(id=id)
        s_date = udata.start_date
        e_date = udata.end_date
        total_vocation=udata.total_v
        news = s_date.split("-")
        newe = e_date.split("-")
        deacrease=(int(newe[-1])-int(news[-1]))
        udata.status='Approved'
        udata.save()
        udata.total_v=total_vocation-deacrease
        udata.save()
        return redirect(manage_dashboard)
    elif status=='rejected':
        udata = employee.objects.get(id=id)
        udata.status = 'Rejected'
        return redirect(manage_dashboard)
def userrequest(request,name):
    data=employee.objects.filter(user=name)
    return render(request, 'manager_dashboard.html', {'all': data})
def manage_dashboard(request):
    pendings=employee.objects.filter(status='Pending')
    status = request.GET.get('request')
    if status=='approved':
        approve_r = employee.objects.filter(status__icontains='approved')
        return render(request, 'manager_dashboard.html', {'approved': approve_r})
    elif status=='pending':
        pendings = employee.objects.filter(status='Pending')
        return render(request, 'manager_dashboard.html', {'pending': pendings})
    elif status=='rejected':
        rejects = employee.objects.filter(status__icontains='rejected')
        return render(request, 'manager_dashboard.html', {'rejected': rejects})
    elif status=='myteam':
        name=request.user.get_username()
        udata=User.objects.filter(username=name)
        for i in udata:
            uid = i.id
        myteams = employee.objects.exclude(user_id=uid)
        return render(request,'manager_dashboard.html',{'myteam':myteams})
    elif status=='all':
        alldata = employee.objects.all()
        return render(request, 'manager_dashboard.html', {'all': alldata})
    return render(request, 'manager_dashboard.html', {'pending':pendings})
def registration_view(request):
    if request.method=='POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(emp_login_view)
    form=RegisterForm()
    return render(request,'register.html',{'form':form})