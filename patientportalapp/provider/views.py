from django.shortcuts import render,get_object_or_404
from django.http import HttpResponseRedirect,HttpResponse
from django.contrib.auth.models import User
from portal.models import ProviderInfo
from .models import MedPrescription,ProvContactInfo
from .forms import MedPrescriptionAdd,ContactInfoAdd
from portal.models import ProviderInfo,PatientInfo
from patient.models import ContactInfo
from django.utils import timezone
from io import BytesIO
from reportlab.lib.units import inch
from reportlab.lib.pagesizes import letter
from reportlab.platypus import Paragraph,SimpleDocTemplate,Spacer,Table,TableStyle
from reportlab.lib.styles import ParagraphStyle,getSampleStyleSheet
from reportlab.lib.enums import TA_LEFT
from reportlab.lib import colors
import pytz
from datetime import datetime

# Create your views here.

def entermedprescription(request, name):
    if request.user.is_authenticated:
        pv = ProviderInfo.objects.get(name=name)
        if request.method == "POST":
            form = MedPrescriptionAdd(request.POST)
            if form.is_valid():
                pn = form.cleaned_data['pat_name']
                mn = form.cleaned_data['med_name']
                ds = form.cleaned_data['dose']
                su=form.cleaned_data['supply']
                b = form.cleaned_data['by']
                pd = form.cleaned_data['period']
                ai=form.cleaned_data['add_instructions']
                dx = form.cleaned_data['dx_code']
                r = form.cleaned_data['refill']
                l = form.cleaned_data['label']
                g = form.cleaned_data['generic']
                np = MedPrescription(providerinfo=pv, pat_name=pn, med_name=mn, dose=ds,supply=su, by=b,
                                     period=pd, add_instructions=ai, dx_code=dx, refill=r, label=l, generic=g)
                np.save()
                pv.medprescription_set.add(np)
                return HttpResponseRedirect(f"/portal/provider/{name}/{pn}/viewprescription/")
        else:
            form = MedPrescriptionAdd()
        return render(request, "main/entermedprescription.html", {"name": name, "form": form})
    else:
        return HttpResponseRedirect("/accounts/login")
    
def viewprescriptionlist(request,name):
    if request.user.is_authenticated:
        plist=MedPrescription.objects.all()
        n_list=[n.pat_name for n in plist]
        m_list=[m.med_name for m in plist]
        zip_list=zip(n_list,m_list)
        return render(request,'main/medprescriptionlist.html',{"zip_list":zip_list,"name":name})
    else:
        return HttpResponseRedirect("/accounts/login")
        
def viewmedprescription(request,name1,name2,med):
    if request.user.is_authenticated:
        info = get_object_or_404(MedPrescription, pat_name=name2, med_name=med)
        if request.method == "POST":
                role="print"
                form = MedPrescriptionAdd(instance=info)
                return render(request,"main/viewmedprescription.html",{"form":form,"name1":name1, "name2":name2,"med":med,"role":role})             
        else:
            info=MedPrescription.objects.get(pat_name=name2,med_name=med)
            role="view"
            return render(request,"main/viewmedprescription.html",{"info":info,"name":name2,"med":med,"role":role})               
    
    else:
        return HttpResponseRedirect("/accounts/login")

def entercontact(request,name):
    if request.user.is_authenticated:
        p=ProviderInfo.objects.get(name=name)
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
                    np = ContactInfo(providerinfo=p, streetandnumber=sn, city=c, state=s, zip=z,\
                                   country=ct, phone1=p1, phone2=p2, email=e)
                    np.save()
                    p.contactinfo_set.add(np)
                    return HttpResponseRedirect("viewcontact")                
        else:    
                form=ContactInfoAdd
                return render(request,"main/entercontact.html",{"form":form,"name":name}) 
    else:
        # Handle the case where the user is not authenticated
        return HttpResponseRedirect("/accounts/login")        

def viewcontact(request,name):
    if request.user.is_authenticated:
        info=ProviderInfo.objects.get(name=name)
        infov=info.contactinfo_set.all()         
        return render(request, 'main/viewcontact.html', {'info': infov, "name": name})
    else:
        # Handle the case where the user is not authenticated
        return HttpResponseRedirect("/accounts/login")                                         

def printmedprescription(request, name1,name2,med):
    if request.user.is_authenticated: 
        if request.method == "POST":
            form = MedPrescriptionAdd(request.POST)
            if form.is_valid():
                pn = form.cleaned_data['pat_name']
                mn = form.cleaned_data['med_name']
                ds = form.cleaned_data['dose']
                su=form.cleaned_data['supply']
                b = form.cleaned_data['by']
                pd = form.cleaned_data['period']
                ai=form.cleaned_data['add_instructions']
                dx = form.cleaned_data['dx_code']
                r = form.cleaned_data['refill']
                l = form.cleaned_data['label']
                g = form.cleaned_data['generic']
                
                date=datetime.now().strftime("%Y-%m-%d")
                infopv = ProviderInfo.objects.get(name=name1)
                infocpv = ProvContactInfo.objects.get(providerinfo=infopv)
                infopt = PatientInfo.objects.get(name=name2)
                infocpt = ContactInfo.objects.get(patinfo=infopt)

                # Create the PDF
                buffer = BytesIO()
                doc = SimpleDocTemplate(buffer, pagesize=letter)
                styles = getSampleStyleSheet()
                our_tz = pytz.timezone('America/New_York')
                
                # Create a ParagraphStyle for visits
                visit_style = ParagraphStyle(
                    name="VisitStyle",
                    parent=styles["Normal"],
                    fontSize=14,
                    leading=16,
                    spaceBefore=12,
                    spaceAfter=12,
                    alignment=TA_LEFT
                )

                # Create the content list
                story = []

                # Patient Summary
                story.append(Paragraph("PRESCRIPTION", styles["Heading1"]))
                story.append(Paragraph(f"Date: {str(date)}",styles["Heading2"]))

                story.append(Paragraph(f"Prescriber: {infopv.name}",styles["Heading2"]))
                story.append(Paragraph(f"Licesne Number: {infopv.license_number}",styles["Normal"]))
                story.append(Paragraph(f"NPI Number: {infopv.npi_number}",styles["Normal"]))
                story.append(Paragraph(f"DEA Number: {infopv.dea_number}",styles["Normal"]))
                story.append(Paragraph(f"Address: {infocpv.streetandnumber}", styles["Normal"]))   
                story.append(Paragraph(f"         {infocpv.city}, {infocpv.state} {infocpv.zip}",styles["Normal"]))

                story.append(Spacer(1, 12))

                story.append(Paragraph(f"Patient Name: {infopt.name}",styles["Heading2"]))
                story.append(Paragraph(f"Brithdate: {infopt.bdate}",styles["Normal"]))
                story.append(Paragraph(f"Address: {infocpt.streetandnumber}", styles["Normal"]))   
                story.append(Paragraph(f"         {infocpt.city}, {infocpt.state} {infocpt.zip}",styles["Normal"]))

                story.append(Spacer(1, 12))

                story.append(Paragraph("-------------------------------------------------------------------------", styles["Normal"]))

                # Vitals as Tables
                story.append(Paragraph("RX",styles['Heading2']))

                table_data = [
                        [Paragraph("Medicine",styles["Normal"]), Paragraph(mn,styles["Normal"])],
                        [Paragraph("Dose",styles["Normal"]), Paragraph(ds,styles["Normal"])],
                        [Paragraph("by",styles["Normal"]), Paragraph(b,styles["Normal"])],
                        [Paragraph("Period",styles["Normal"]), Paragraph(pd,styles["Normal"])],
                        [Paragraph("Supply",styles["Normal"]), Paragraph(su,styles["Normal"])],
                        [Paragraph("Additional Instructions",styles["Normal"]), Paragraph(ai,styles["Normal"])],
                        [Paragraph("DX ",styles["Normal"]), Paragraph(dx,styles["Normal"])],
                        [Paragraph("Refills",styles["Normal"]), Paragraph(str(r),styles["Normal"])],
                        [Paragraph("Label",styles["Normal"]), " "],
                        [Paragraph("Generic",styles["Normal"]), " "]
                    ]
                    
                if l == True: 
                    table_data[8][1] = "\u2713"  
                        
                if g == True:
                    table_data[9][1] = "\u2713"  


                    # Create the table
                table = Table(table_data, colWidths=[2.5 * inch, 2.5* inch])

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
                story.append(Spacer(1, 12))  # Add some space between tables
                story.append(Spacer(1, 12))  # Add some space between tables

                # Separator before visits
                story.append(Paragraph("Signature:__________________________________________________", styles["Normal"]))
            
                story.append(Spacer(1, 12))  # Add some space between tables

                # Build the PDF
                doc.build(story)

                response = HttpResponse(buffer.getvalue(), content_type='application/pdf')
                response['Content-Disposition'] = 'attachment; filename="prescript.pdf"'
                return response
        else:
            return HttpResponse("Not Valid Request...")    
    else:
        return HttpResponseRedirect("/accounts/login")  


