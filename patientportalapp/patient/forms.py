from django import forms
from .models import PatientInfo,ContactInfo,EmergencyContact,InsuranceInfo,Visit,Vitals


class VitalsAdd(forms.ModelForm):
    class Meta:
        model = Vitals
        fields = ('time','height','weight','temperature','resp_rate','pulse','oxy_sat','blood_pressure')
        labels={"time":"Date and Time (e.g. YYYY-MM-YY hr:mi:sec)",
                "height":"Height (e.g. FT-IN)",
                "weight":"Weight (pounds)",
                "temperature":"Temperature (degrees F)",
                "resp_rate":"Respiration Rate (breaths/minute)",
                "pulse":"Pulse Rate (beats/minute)",
                "oxy_sat":"O2 Saturation",
                "blood_pressure":"Blood Pressure (Systolic/Diastolic mmHg)",}
        
class VisitAdd(forms.ModelForm):
    class Meta:
        model = Visit
        fields = ('time','reason','dx','px','lx','prx','patinst')
        labels={"time":"Date and Time (e.g. YYYY-MM-DD hr:mi:sec)",
                "reason":"Reason of Visit",
                "dx":"Diagnosis",
                "px":"Perscriptions",
                "lx":"Labs Ordered",
                "prx":"Procedures Ordered",
                "patinst":"Patient Instructions",}  

class ContactInfoAdd(forms.ModelForm):
    class Meta:
        model=ContactInfo
        fields=['streetandnumber','city','state','zip', 'country','phone1','phone2','email']
        labels={'streetandnumber':"Address (e.g. Street Number and Street, Apartment/Unit)",
                "city":'City',
                'state':'State',
                'zip':'Zip or Postal Code',
                'country':'Country',
                'phone1':'Primary Phone Number (e.g.+1XXXXXXXXXX)',
                'phone2':'Secondary Phone Number (e.g.+1XXXXXXXXXX)',
                'email':'Email',}

class EmergencyContactAdd(forms.ModelForm):
    class Meta:
        model=EmergencyContact
        fields=['emergency_contact','relation','streetandnumber','city','state','zip', 'country','phone1','phone2','email']
        labels={'emergency_contct':'Name of Emergency Contact',
                'relation':'Relationship to Patient',
                'streetandnumber':'Address (e.g. Street Number and Street, Apartment/Unit)',
                "city":'City',
                'state':'State',
                'zip':'Zip or Postal Code',
                'country':'Country',
                'phone1':'Primary Phone Number (e.g.+1XXXXXXXXXX)',
                'phone2':'Secondary Phone Number (e.g.+1XXXXXXXXXX)',
                'email':'Email',}         

class InsuranceAdd(forms.ModelForm):
    class Meta:
        model=InsuranceInfo
        fields=['insurance_company','groupandnumber','streetandnumber','city','state','zip', 'country','phone','fax','email']
        labels={'insurance_company':'Name of Insurance Company',
                'groupandnumber':'Provider Group and ID Number',
                'streetandnumber':"Address (e.g. Street Number and Street, Apartment/Unit)",
                "city":'City',
                'state':'State',
                'zip':'Zip or Postal Code',
                'country':'Country',
                'phone':'Phone Number (e.g.+1XXXXXXXXXX)',
                'fax':'Fax Number (e.g.+1XXXXXXXXXX)',
                'email':'Email',}      