from django.shortcuts import render
from django.http import HttpResponse,HttpResponseRedirect
from django.contrib.auth.models import User
from .models import Vitals,Visit
from .models import PatientInfo,ContactInfo,EmergencyContact,InsuranceInfo
from .forms import VisitAdd,VitalsAdd
from .forms import EmergencyContactAdd,ContactInfoAdd,InsuranceAdd
from io import BytesIO
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
from reportlab.lib.pagesizes import letter
from reportlab.platypus import Paragraph,SimpleDocTemplate,Spacer,Table,TableStyle
from reportlab.lib.styles import ParagraphStyle,getSampleStyleSheet
from reportlab.lib.enums import TA_LEFT
from reportlab.lib import colors
import datetime
import plotly.graph_objects as go
import plotly.io as pio
import json
import pytz

# Create your views here.

#enter vitals for a patient
def entervitals(request,name):
    if request.user.is_authenticated:
        p=PatientInfo.objects.get(name=name)
        if request.method=="POST":
                form=VitalsAdd(request.POST)
                if form.is_valid():
                    d=form.cleaned_data['time']
                    h=form.cleaned_data["height"]
                    w=form.cleaned_data["weight"]
                    t=form.cleaned_data["temperature"]
                    r=form.cleaned_data["resp_rate"]
                    pu=form.cleaned_data["pulse"]
                    o=form.cleaned_data["oxy_sat"]
                    b=form.cleaned_data["blood_pressure"]
                    np = Vitals(patinfo=p, time=d, height=h, weight=w, temperature=t, resp_rate=r, pulse=pu, oxy_sat=o, blood_pressure=b)
                    np.save()
                    p.vitals_set.add(np)
                    return HttpResponseRedirect("/portal/patient/"+str(name)+"/viewvitals/")                
        else:    
                form=VitalsAdd
                return render(request,"main/entervitals.html",{"form":form,"name":name}) 
    else:
        # Handle the case where the user is not authenticated
        return HttpResponseRedirect("/accounts/login")
    
# enter vist for a patient
def entervisit(request,name):
    if request.user.is_authenticated:
        p=PatientInfo.objects.get(name=name)
        if request.method=="POST":
                form=VisitAdd(request.POST)
                if form.is_valid():
                    t=form.cleaned_data["time"]
                    r=form.cleaned_data["reason"]
                    d=form.cleaned_data["dx"]
                    p=form.cleaned_data["px"]
                    l=form.cleaned_data["lx"]
                    pr=form.cleaned_data["prx"]
                    i=form.cleaned_data["patinst"]
                    np = Visit(PatientInfo=p, time=t, reason=r, dx=d, px=p, lx=l, prx=pr,patinst=i)
                    np.save()
                    p.patvisit_set.add(np)
                    return HttpResponseRedirect("/"+str(name)+"/viewvisits/")                
        else:    
                form=VisitAdd
                return render(request,"main/entervisit.html",{"form":form,"name":name}) 
    else:
        # Handle the case where the user is not authenticated
        return HttpResponseRedirect("/accounts/login")    
    
def entercontact(request,name):
    if request.user.is_authenticated:
        p=PatientInfo.objects.get(name=name)
        if request.method=="POST":
                form=ContactInfoAdd(request.POST)
                if form.is_valid():
                    sn=form.cleaned_data["streetandnumber"]
                    c=form.cleaned_data["city"]
                    s=form.cleaned_data["state"]
                    z=form.cleaned_data["zip"]
                    ct=form.cleaned_data['country']
                    p1=form.cleaned_data["phone1"]
                    p2=form.cleaned_data['phone2']
                    e=form.cleaned_data["email"]
                    np = ContactInfo(patinfo=p, streetandnumber=sn, city=c, state=s, zip=z,\
                                   country=ct, phone1=p1, phone2=p2, email=e)
                    np.save()
                    p.contactinfo_set.add(np)
                    return HttpResponseRedirect("portal/patient/"+str(name)+"/viewcontact/")                
        else:    
                form=ContactInfoAdd
                return render(request,"main/entercontact.html",{"form":form,"name":name}) 
    else:
        # Handle the case where the user is not authenticated
        return HttpResponseRedirect("/accounts/login")       

def enteremergencycontact(request,name):
    if request.user.is_authenticated:
        p=PatientInfo.objects.get(name=name)
        if request.method=="POST":
                form=EmergencyContactAdd(request.POST)
                if form.is_valid():
                    en=form.cleaned_data['emergency_contact']
                    r=form.cleaned_data['relation']
                    sn=form.cleaned_data["streetandnumber"]
                    c=form.cleaned_data["city"]
                    s=form.cleaned_data["state"]
                    z=form.cleaned_data["zip"]
                    ct=form.cleaned_data['country']
                    p1=form.cleaned_data["phone1"]
                    p2=form.cleaned_data['phone2']
                    e=form.cleaned_data["email"]
                    np = EmergencyContact(patinfo=p, emergency_contact=en, relation=r, streetandnumber=sn, city=c, state=s, zip=z,\
                                   country=ct, phone1=p1, phone2=p2, email=e)
                    np.save()
                    p.emergencycontact_set.add(np)
                    return HttpResponseRedirect("/portal/patient/"+str(name)+"/viewecontact/")                
        else:    
                form=EmergencyContactAdd
                return render(request,"main/enterecontact.html",{"form":form,"name":name}) 
    else:
        # Handle the case where the user is not authenticated
        return HttpResponseRedirect("/accounts/login")  

def enterinsurance(request,name):
    if request.user.is_authenticated:
        p=PatientInfo.objects.get(name=name)
        if request.method=="POST":
                form=InsuranceAdd(request.POST)
                if form.is_valid():
                    i=form.cleaned_data['insurance_company']
                    gn=form.cleaned_data['groupandnumber']
                    sn=form.cleaned_data["streetandnumber"]
                    c=form.cleaned_data["city"]
                    s=form.cleaned_data["state"]
                    z=form.cleaned_data["zip"]
                    ct=form.cleaned_data['country']
                    p1=form.cleaned_data["phone"]
                    f=form.cleaned_data['fax']
                    e=form.cleaned_data["email"]
                    np = InsuranceInfo(patinfo=p, insurance_company=i, groupandnumber=gn, streetandnumber=sn, city=c, state=s, zip=z,\
                                   country=ct, phone=p1,fax=f, email=e)
                    np.save()
                    p.insuranceinfo_set.add(np)
                    return HttpResponseRedirect("/protal/patient/"+str(name)+"/viewinsurance/")                
        else:    
                form=InsuranceAdd
                return render(request,"main/enterinsurance.html",{"form":form,"name":name}) 
    else:
        # Handle the case where the user is not authenticated
        return HttpResponseRedirect("/accounts/login")
    
# view a vitals list and interactive plot of vitals over time      
def viewvitals(request, name):
    if request.user.is_authenticated:
        info=PatientInfo.objects.get(name=name)
        infov = info.vitals_set.all().order_by('time')

        x_data = [instance.time.isoformat() for instance in infov]
        x_range=range(len(x_data))
        vitals_data = [
            [float(instance.height_inch) for instance in infov],
            [float(instance.weight) for instance in infov],
            [float(instance.bmi) for instance in infov],
            [float(instance.temperature) for instance in infov],
            [float(instance.resp_rate) for instance in infov],
            [float(instance.pulse) for instance in infov],
            [float(instance.oxy_sat) for instance in infov],
            [float(instance.blood_pres[0]) for instance in infov],  # Systolic
            [float(instance.blood_pres[1]) for instance in infov]  # Diastolic
        ]
        vitals_name = [
            "Height (Inches)",
            "Weight (Pounds)",
            "BMI (Pounds/Square Inch)",
            "Temperature (degrees F)",
            "Repiration Rate (breaths/minute)",
            "Pulse (Heartbeats/minute)",
            "O2 Saturation (Percent)",
            "Systolic (mmHg)",
            "Diastolic (mmHg)"
        ]

        vitals_label = [
            "Height (Inches)",
            "Weight (Pounds)",
            "BMI (Pounds/Square Inch)",
            "Temperature (degrees F)",
            "Repiration Rate (breaths/minute)",
            "Pulse (Heartbeats/minute)",
            "O2 Saturation (Percent)",
            "Systolic\Disatolic (mmHg)"
        ]


        vitals_show = [True,False, False, False, False, False, False, False, False]

        vitals_update = [
            [True, False, False, False, False, False, False, False, False, True, False, False, False, False, False, False, False, False, True, False, False, False, False, False, False, False, False],
            [False, True, False, False, False, False, False, False, False, False, True, False, False, False, False, False, False, False, False, True, False, False, False, False, False, False, False],
            [False, False, True, False, False, False, False, False, False, False, False, True, False, False, False, False, False, False, False, False, True, False, False, False, False, False, False],
            [False, False, False, True, False, False, False, False, False, False, False, False, True, False, False, False, False, False, False, False, False, True, False, False, False, False, False],
            [False, False, False, False, True, False, False, False, False, False, False, False, False, True, False, False, False, False, False, False, False, False, True, False, False, False, False],
            [False, False, False, False, False, True, False, False, False, False, False, False, False, False, True, False, False, False, False, False, False, False, False, True, False, False, False],
            [False, False, False, False, False, False, True, False, False, False, False, False, False, False, False, True, False, False, False, False, False, False, False, False, True, False, False],
            [False, False, False, False, False, False, False, True, True, False, False, False, False, False, False, False, True, True, False, False, False, False, False, False, False, True, True] 
        ]

        min_limits = [
            65, 140, 20, 97, 12, 60, 95, 100, 60 
        ]
        max_limits = [
            72, 200, 30, 100, 20, 100, 100, 140, 90
        ]

        fig = go.Figure(
            data=[
                go.Scatter(x=x_data, y=i, name=j, mode='lines', visible=k)
                for i, j, k in zip(vitals_data, vitals_name, vitals_show)
            ] + [  # Add min and max lines
                go.Scatter(x=x_data, y=[j] * len(x_data), mode='lines', line_color="red", line=dict(dash="dash"),visible=k, name=f"{vitals_name[i]} Lower Limit") 
                for i, (j, k) in enumerate(zip(min_limits, vitals_show))
            ] + [
                go.Scatter(x=x_data, y=[j] * len(x_data), mode='lines', line_color="red", line=dict(dash="dash") ,visible=k, name=f"{vitals_name[i]} Upper Limit") 
                for i, (j, k) in enumerate(zip(max_limits, vitals_show))
            ],
            layout=go.Layout(
                title=str(name) + "'s Vitals",
                xaxis_title="Time",
                yaxis_title="Vitals",
                updatemenus=[
                    dict(
                        active=0,
                        buttons=[
                            dict(label=l,
                                 method="update",
                                 args=[{"visible": m,}]) for l,m in zip(vitals_label,vitals_update)],
                        direction="down",
                        xanchor="left",
                        yanchor="top",
                        x=0.65,
                        y=1.25
                    )
                ]
            )
        )
        
        graph_json = fig.to_json()  # Use fig.to_json() for serialization
        context = {'info': infov, 'name': name, 'graph_json': graph_json}
        return render(request, 'main/viewvitals.html', context)
    else:
        return HttpResponseRedirect("/accounts/login")

# view a list of a patients visits over time    
def viewvisits(request,name):
    if request.user.is_authenticated:
        info=PatientInfo.objects.get(name=name)
        infov=info.visit_set.all()         
        return render(request, 'main/viewvisits.html', {'info': infov, "name": name})
    else:
        # Handle the case where the user is not authenticated
        return HttpResponseRedirect("/accounts/login")
    
#view patient contact information
def viewcontact(request,name):
    if request.user.is_authenticated:
        info=PatientInfo.objects.get(name=name)
        infov=info.contactinfo_set.all()         
        return render(request, 'main/viewcontact.html', {'info': infov, "name": name})
    else:
        # Handle the case where the user is not authenticated
        return HttpResponseRedirect("/accounts/login")
    
    
#view patient emergency contact information
def viewecontact(request,name):
    if request.user.is_authenticated:
        info=PatientInfo.objects.get(name=name)
        infov=info.emergencycontact_set.all()       
        return render(request, 'main/viewecontact.html', {'info': infov, "name": name})
    else:
        # Handle the case where the user is not authenticated
        return HttpResponseRedirect("/accounts/login")    

#view patient insurance information
def viewinsurance(request,name):
    if request.user.is_authenticated:
        info=PatientInfo.objects.get(name=name)
        infov=info.emergencycontact_set.all()        
        return render(request, 'main/viewcontact.html', {'info': infov, "name": name})
    else:
        # Handle the case where the user is not authenticated
        return HttpResponseRedirect("/accounts/login") 

# creates a patient summary with all the vitals, visits, information for the patient
# in a .pdf html response
def patientsummary(request, name):
    if request.user.is_authenticated:  
        info = PatientInfo.objects.get(name=name)
        infoc = ContactInfo.objects.get(patinfo=info)
        infovt = info.vitals_set.all().order_by('time')  # Order vitals by date/time
        infovs = info.visit_set.all().order_by('time')

        # Create the PDF
        buffer = BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=letter)
        styles = getSampleStyleSheet()
        our_tz = pytz.timezone('America/New_York')
        
        # Create a ParagraphStyle for visits
        visit_style = ParagraphStyle(
            name="VisitStyle",
            parent=styles["Normal"],
            fontSize=12,
            leading=16,
            spaceBefore=12,
            spaceAfter=12,
            alignment=TA_LEFT
        )

        # Create the content list
        story = []

        # Patient Summary
        story.append(Paragraph("Patient Summary for " + str(name), styles["Heading1"]))
        story.append(Paragraph(f"ID: {info.pid}",styles["Heading2"]))

        story.append(Paragraph("Demographic Information:",styles["Heading2"]))
        story.append(Paragraph(f"Brithdate (Age): {info.bdate} ({info.age} years)",styles["Normal"]))
        story.append(Paragraph(f"Gender: {info.gender}", styles["Normal"]))   
        story.append(Paragraph(f"History: {info.hist}",styles["Normal"]))

        story.append(Spacer(1, 12))

        providers = info.provider.all()
        if providers:
            story.append(Paragraph("Provider(s):", styles["Heading2"]))
            for provider in providers:
                story.append(Paragraph(provider.name, styles["Normal"]))
        else:
                story.append(Paragraph("None", styles["Normal"]))

        story.append(Spacer(1, 12))

        story.append(Paragraph("Contact Information:",styles["Heading2"]))
        story.append(Paragraph(infoc.streetandnumber,styles["Normal"]))
        story.append(Paragraph(f"{infoc.city}, {infoc.state} {infoc.zip}", styles["Normal"]))
        story.append(Paragraph(str(infoc.phone1),styles["Normal"]))

        story.append(Spacer(1, 12))

        story.append(Paragraph("-------------------------------------------------------------------------", styles["Normal"]))

        # Vitals as Tables
        story.append(Paragraph("Vitals", styles["Heading2"]))
        for pt in infovt:
            table_data = [
                ["Time", pt.time.astimezone(our_tz).strftime('%B %d, %Y at %I:%M %p')],
                ["Height", pt.height],
                ["Weight", pt.weight],
                ["Temperature", pt.temperature],
                ["Respiration", pt.resp_rate],
                ["Pulse", pt.pulse],
                ["Oxygen Saturation", pt.oxy_sat],
                ["Blood Pressure", pt.blood_pressure]
            ]

            # Create the table
            table = Table(table_data, colWidths=[1.5 * inch, 2.5* inch])

            # Apply a simple table style
            table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.lightgrey),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.black),
                ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, 0), 12),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                ('INNERGRID', (0, 0), (-1, -1), 0.25, colors.black),
                ('BOX', (0, 0), (-1, -1), 0.25, colors.black),
            ]))

            story.append(table)
            story.append(Spacer(1, 12))  # Add some space between tables

        # Separator before visits
        story.append(Paragraph("------------------------------------------------------------------------", styles["Normal"]))
        story.append(Paragraph("Visits", styles["Heading2"]))

        # Add visits data using the custom style and table format
        for pt in infovs:
            table_data = [
                ["Time", pt.time.astimezone(our_tz).strftime('%B %d, %Y at %I:%M %p')],
                ["Reason for Visit", Paragraph(pt.reason)],
                ["Diagnosis", Paragraph(pt.dx)],
                ["Perscriptions", Paragraph(pt.px)],
                ["Laboratories Ordered", Paragraph(pt.lx)],
                ["Procedures Ordered", Paragraph(pt.prx)],
                ["Patient Instructions", Paragraph(pt.patinst)]
            ]

            # Create the table
            table = Table(table_data, colWidths=[1.5 * inch, 3 * inch])

            # Apply a simple table style
            table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.lightgrey),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.black),
                ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                ('VALIGN',(0,0),(-1,-1),'TOP'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, 0), 12),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                ('INNERGRID', (0, 0), (-1, -1), 0.25, colors.black),
                ('BOX', (0, 0), (-1, -1), 0.25, colors.black),
            ]))

            story.append(table)
            story.append(Spacer(1, 12))  # Add some space between tables

        # Build the PDF
        doc.build(story)

        response = HttpResponse(buffer.getvalue(), content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="vitals.pdf"'
        return response
    else:
        return HttpResponseRedirect("/accounts/login")       



