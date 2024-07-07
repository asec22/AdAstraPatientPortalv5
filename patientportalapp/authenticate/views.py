from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import RegisterForm
from portal.models import PatientInfo, ProviderInfo, AdministratorInfo
from django.contrib.auth.models import User,Group

def register(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            l = form.cleaned_data['last_name']
            f = form.cleaned_data['first_name']
            gr = form.cleaned_data['groups']
            g=gr.name
            fname = " ".join([f, l])
            
            # Check if the user exists in the relevant database with matching group
            if g == "Patient":
                try:
                    patient = PatientInfo.objects.get(name=fname).group
                    print(patient)
                    if g==patient:
                        user = form.save(commit=False)  # Save the user object but don't commit to the database yet
                        user.save()  # Save the user object to the database
                        user.groups.add(gr)  # Save the user only if validation passes
                        return redirect('success')
                    else:
                        messages.error(request, "Group attribute does not match.")
                except PatInfo.DoesNotExist:
                    messages.error(request, "Patient not found in the database.")
            
            elif g == "Provider":
                try:
                    provider = ProviderInfo.objects.get(name=fname).group
                    if g==provider:
                        user = form.save(commit=False)  # Save the user object but don't commit to the database yet
                        user.save()  # Save the user object to the database
                        user.groups.add(gr)  # Save the user only if validation passes
                        return redirect('success')
                    else:
                        messages.error(request, "Group attribute does not match.")
                except ProviderInfo.DoesNotExist:
                    messages.error(request, "Provider not found in the database.")
            
            elif g == "Administrator":
                try:
                    admin = AdministratorInfo.objects.get(name=fname).group
                    if g==admin:
                        user = form.save(commit=False)  # Save the user object but don't commit to the database yet
                        user.save()  # Save the user object to the database
                        user.groups.add(gr)  # Save the user only if validation passes
                        return redirect('success')
                    else:
                        messages.error(request, "Group attribute does not match.")
                except AdministratorInfo.DoesNotExist:
                    messages.error(request, "Administrator not found in the database.")
            
            else:
                messages.error(request, "Invalid group selection.")
        
        # If the form is not valid or any error occurs, render the form again with errors
        return render(request, "register/register.html", {"form": form})
    
    else:
        form = RegisterForm()
        return render(request, "register/register.html", {"form": form})

def success(request):
    return render(request, "register/success.html", {})

def nosuccess(request):
    return render(request, "register/nosuccess.html", {})
