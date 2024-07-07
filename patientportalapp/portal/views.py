from django.shortcuts import render
from django.http import HttpResponse,HttpResponseRedirect
from .models import PatientInfo,ProviderInfo,AdministratorInfo
from .forms import PatientAdd,ProviderAdd,AdministratorAdd

# create your views here

# portal pages based on user group
def portal(request):
    if request.user.is_authenticated:
        u=request.user
        name=" ".join([u.first_name,u.last_name])
        return render(request,"main/portal.html",{"name":name})
    else:
        return HttpResponseRedirect("/accounts/login")

#create a new patient in the medical practice
def createpat(request):
    if request.user.is_authenticated:
        if request.method=="POST":
            form=PatientAdd(request.POST)
            if form.is_valid():
                np = form.save(commit=False)
                np.save()  # Save the instance to get an ID
                form.save_m2m()  # Save the many-to-many data for the form
            return HttpResponseRedirect("/portal")    
        else:    
            form=PatientAdd
        return render(request,"main/createpat.html",{"form":form})
    else:
        return HttpResponseRedirect("/accounts/login")
    
def createprov(request):
    if request.user.is_authenticated:
        if request.method=="POST":
            form=ProviderAdd(request.POST)
            if form.is_valid():
                n=form.cleaned_data["name"]
                r=form.cleaned_data["role"]
                ln=form.cleaned_data["license_number"]
                nn=form.cleaned_data["npi_number"]
                np=ProviderInfo(name=n,role=r,license_number=ln,npi_number=nn)
                np.save()
            return HttpResponseRedirect("/portal")    
        else:    
            form=ProviderAdd
        return render(request,"main/createprov.html",{"form":form})
    else:
        return HttpResponseRedirect("/accounts/login")

def createad(request):
    if request.user.is_authenticated:
        if request.method=="POST":
            form=AdministratorAdd(request.POST)
            if form.is_valid():
                n=form.cleaned_data["name"]
                r=form.cleaned_data["role"]
                ln=form.cleaned_data["license_number"]
                nn=form.cleaned_data["npi_number"]
                dn=form.cleaned_data['dea_number']
                np=AdministratorInfo(name=n,role=r,license_number=ln,npi_number=nn,dea_number=dn)
                np.save()
            return HttpResponseRedirect("/portal")    
        else:    
            form=AdministratorAdd
        return render(request,"main/createad.html",{"form":form})
    else:
        return HttpResponseRedirect("/accounts/login")        

# view the patient list for a specific doctor
def viewpatlist(request):
    if request.user.is_authenticated:
        patlist=PatientInfo.objects.all()
        return render(request, 'main/viewpatlist.html', {'patlist': patlist})
    else:
        # Handle the case where the user is not authenticated
        return HttpResponseRedirect("/accounts/login")
    
def viewprovlist(request):
    if request.user.is_authenticated:
        provlist=ProviderInfo.objects.all()
        return render(request, 'main/viewprovlist.html', {'provlist': provlist})
    else:
        # Handle the case where the user is not authenticated
        return HttpResponseRedirect("/accounts/login")  

def viewadlist(request):
    if request.user.is_authenticated:
        adlist=AdministratorInfo.objects.all()
        return render(request, 'main/viewadlist.html', {'adlist': adlist})
    else:
        # Handle the case where the user is not authenticated
        return HttpResponseRedirect("/accounts/login")       

# view a specific patient's base information 
# Full Name, Date of Birth, Age, Gender, and History
def viewpatinfo(request, name):
    if request.user.is_authenticated:
        if request.user.groups.filter(name='Patient').exists():
           role="patient"
        else:
            role="other"  
        info=PatientInfo.objects.get(name=name)
        context = {'info': info, 'role': role}
        return render(request, 'main/viewpatinfo.html', context)
    else:
        # Handle the case where the user is not authenticated
        return HttpResponseRedirect("/accounts/login")
    
def viewprovinfo(request, name):
    if request.user.is_authenticated:
        info=ProviderInfo.objects.get(name=name)
        context = {'info': info}
        return render(request, 'main/viewprovinfo.html', context)
    else:
        # Handle the case where the user is not authenticated
        return HttpResponseRedirect("/accounts/login") 

def viewadinfo(request, name):
    if request.user.is_authenticated:
        info=AdministratorInfo.objects.get(name=name)
        context = {'info': info}
        return render(request, 'main/viewadinfo.html', context)
    else:
        # Handle the case where the user is not authenticated
        return HttpResponseRedirect("/accounts/login")       


