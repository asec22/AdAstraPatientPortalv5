from django import forms
from .models import MedPrescription,ProvContactInfo
from portal.models import PatientInfo

#create your forms here

class MedPrescriptionAdd(forms.ModelForm):
    pat_name=forms.ModelChoiceField(queryset=PatientInfo.objects.all())

    class Meta:
        model=MedPrescription
        fields=['pat_name','med_name','dose','supply','by','period','add_instructions','dx_code','refill','label','generic']
        labels={
            "pat_name":"Patient Name",
            "med_name":"Medicine Name",
            "dose":"Dose",
            "by":"By",
            "period":"Period/Frequency",
            'add_instructions':'Additonal Warnings/Instructions',
            "dx_code":"Diagnosis Code",
            "refill":"Refils",
            "label":"Label",
            "generic":"Generic",}
        
class ContactInfoAdd(forms.ModelForm):
    class Meta:
        model=ProvContactInfo
        fields=['streetandnumber','city','state','zip', 'country','phone1','phone2','email']
        labels={'streetandnumber':"Address (e.g. Street Number and Street, Apartment/Unit)",
                "city":'City',
                'state':'State',
                'zip':'Zip or Postal Code',
                'country':'Country',
                'phone1':'Primary Phone Number (e.g.+1XXXXXXXXXX)',
                'phone2':'Secondary Phone Number (e.g.+1XXXXXXXXXX)',
                'email':'Email',}