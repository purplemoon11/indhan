from django.core import paginator
from django.shortcuts import render, redirect, HttpResponseRedirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
import mysql.connector as sql
import json
from django.http import JsonResponse, HttpResponse
from django.core.paginator import Paginator
from django.template.loader import get_template
from xhtml2pdf import pisa
import datetime

from xhtml2pdf.parser import HTML2PDF

# Create your views here.
from .models import *
from .forms import CreateUserForm, update


# Register Function
def registerPage(request):
    if request.user.is_authenticated:
        return redirect('home')
    else:
        form = CreateUserForm()
        if request.method == 'POST':
            form = CreateUserForm(request.POST)
            if form.is_valid():
                form.save()
                user = form.cleaned_data.get('username')
                messages.success(request, 'Account was created for ' + user)

                return redirect('login')

        context = {'form': form}
        return render(request, 'accounts/register.html', context)

# Login Function
def loginPage(request):
    if request.user.is_authenticated:
        return redirect('home')
    else:
        if request.method == 'POST':
            username = request.POST.get('username')
            password = request.POST.get('password')

            user = authenticate(request, username=username, password=password)

            if user is not None and user.is_superuser:
                login(request, user)
                return redirect('adminpage')
            
            if user is not None:
                login(request, user)
                return redirect('home')

            else:
                messages.info(request, "Username or password is incorrect")

        context = {}
        return render(request, 'accounts/login.html', context)

# LogOut Function
def logoutUser(request):
    logout(request)
    return redirect('login')


@login_required(login_url='login')
# DashBoard/Home Function
def homePage(request):
    data = Entry.objects.all().count()
    result = (Entry.objects.all().order_by('-Gasoline')[:5])
    context = {"data":data,
               "result":result  
              }
    return render(request, 'accounts/home.html', context)


@login_required(login_url='login')
# Entry Function
def entryPage(request):
    saverecord = update()
    if request.method == 'POST':
        saverecord = update(request.POST)
        if saverecord.is_valid():
            saverecord.save()
            return redirect('/entry')
    else:
        context = {}
    return render(request, 'accounts/entry.html', context)


@login_required(login_url='login')
# Report Funtion
def reportPage(request):
    report = Entry.objects.get_queryset().order_by('-id')
    i = 1
    paginator = Paginator(report, 5)
    page_number = request.GET.get('page')
    page_obj = Paginator.get_page(paginator, page_number) 
    context = {
        'rp': report,
        'page_obj': page_obj
    }
    return render(request, 'accounts/report.html', context)

@login_required(login_url='login')
# Update Funtion
def updatePage(request, id):
    pi = Entry.objects.get(id=id)
    # form = update(request.POST)

    if request.method == 'POST':
        pi.name = request.POST.get('name')
        pi.Gasoline_type = request.POST.get('Gasoline_type')
        pi.Gasoline = request.POST.get('Gasoline')
        pi.date = request.POST.get('date')
        pi.vehicle_number = request.POST.get('vehicle_number')
        pi.purpose = request.POST.get('purpose')
        pi.type = request.POST.get('type')

        if checkDataValidity(pi):
            pi.save()
            return redirect('/report')
        else:
            messages.error(request, "Error in data")

    return render(request, 'accounts/update.html', {'pi':pi})

# Admin function
def adminPage(request):
    data = Entry.objects.all().count()
    result = (Entry.objects.all().order_by('-Gasoline')[:5])
    context = {"data":data,
               "result":result  
              }
    return render(request, 'accounts/adminpage.html', context)


@login_required(login_url='login')
def adminEntry(request):
    saverecord = update()
    if request.method == 'POST':
        saverecord = update(request.POST)
        if saverecord.is_valid():
            saverecord.save()
            return redirect('/adminentry')
    else:
        context = {}
    return render(request, 'accounts/adminentry.html', context)

@login_required(login_url='login')
def adminReport(request):
    report = Entry.objects.get_queryset().order_by('-id')
    i = 1
    paginator = Paginator(report, 5)
    page_number = request.GET.get('page')
    page_obj = Paginator.get_page(paginator, page_number)
    context = {
        'rp': report,
        'page_obj': page_obj
    }
    return render(request, 'accounts/adminreport.html', context)

# Search for admin and client
@login_required(login_url='login')
def search_list(request):
    if request.method == "POST":
        search_str = json.loads(request.body).get('searchText')
        entry = Entry.objects.filter(
            vehicle_number__istartswith=search_str) | Entry.objects.filter(
            Gasoline_type=search_str) | Entry.objects.filter(
            Gasoline=search_str) | Entry.objects.filter(
            purpose=search_str) | Entry.objects.filter(
            date__istartswith=search_str) | Entry.objects.filter(
            name__istartswith=search_str)

        data = entry.values()
        return JsonResponse(list(data), safe=False)

#Result Deletion
@login_required(login_url='login')
def deletePage(request, id):
    if request.method == "POST":
        pi = Entry.objects.get(pk=id)
        pi.delete()
    return redirect('adminreport')

#Update
@login_required(login_url='login')
def adminUpdate(request, id):
    pi = Entry.objects.get(id=id)
    # form = update(request.POST)

    if request.method == 'POST':
        pi.name = request.POST.get('name')
        pi.Gasoline_type = request.POST.get('Gasoline_type')
        pi.Gasoline = request.POST.get('Gasoline')
        pi.date = request.POST.get('date')
        pi.vehicle_number = request.POST.get('vehicle_number')
        pi.purpose = request.POST.get('purpose')
        pi.type = request.POST.get('type')
        
        if checkDataValidity(pi):
            pi.save()
            return redirect('/adminreport')
        else:
            messages.err(request, "Error in data")

    return render(request, 'accounts/adminupdate.html', {'pi':pi})

# Check validity of data
def checkDataValidity(data):
    if data.name == None or data.name == "":
        return False;
    if data.Gasoline_type == None or data.Gasoline_type == "":
        return False;
    if data.Gasoline == None or data.Gasoline == "":
        return False;
    if data.date == None or data.date == "":
        return False;
    if data.vehicle_number == None or data.vehicle_number == "":
        return False;
    if data.purpose == None or data.purpose == "":
        return False;
    if data.type == None or data.type == "":
        return False;
    return True
 
#print to pdf
""" def render_pdf_view(request, *args, **kwargs):
    id = kwargs.get('id')
    entry = get_object_or_404(Entry, id=id)
    template_path = 'accounts/print.html'
    context = {'entry': entry}
    # Create a Django response object, and specify content_type as pdf
    response = HttpResponse(content_type='application/pdf')
    #if download
    #response['Content-Disposition'] = 'attachment; filename="report.pdf"'
    response['Content-Disposition'] = 'filename="report.pdf"'
    # find the template and render it.
    template = get_template(template_path)
    html = template.render(context)

    # create a pdf
    pisa_status = pisa.CreatePDF(html.encode('UTF-8'), dest=response, encoding='UTF-8')
    # if error then show some funy view
    if pisa_status.err:
       return HttpResponse('We had some errors <pre>' + html + '</pre>')
    return response
 """
#filtering Data
@login_required(login_url='login')
def adminPublish(request):
    if request.method == "POST":
        fromdate = request.POST.get('fromdate')
        todate = request.POST.get('todate')
        searchResult = Entry.objects.raw('select id, name, Gasoline_type, Gasoline, date, vehicle_number, purpose from entry where date between "'+fromdate+'" and "'+todate+'"')
        return render(request, 'accounts/adminPublish.html', {'data': searchResult})
    else:
        report = Entry.objects.all()
        context = {
            'rp': report
        }
        return render(request, 'accounts/adminPublish.html', context)

@login_required(login_url='login')
def test(request, id):
    pi = Entry.objects.get(id=id)
    return render(request, 'accounts/test.html', {'pi':pi})
