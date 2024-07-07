from django import forms
from .models import PatientInfo,ProviderInfo,AdministratorInfo

class PatientAdd(forms.ModelForm):
    provider = forms.ModelMultipleChoiceField(
        queryset=ProviderInfo.objects.none(),
        widget=forms.CheckboxSelectMultiple,  # optional: use checkboxes for multiple selections
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['provider'].queryset = ProviderInfo.objects.filter(
            role__in=["Doctor", "Physician Assistant", "Nurse Practitioner"]
        )

    class Meta:
        model = PatientInfo
        fields = ('name', 'bdate', 'gender', 'provider', 'hist')
        labels = {
            "name": "Patient Full Name",
            "bdate": "Patient's Birthdate (e.g., YYYY-MM-DD)",
            "gender": "Gender (M/F/O)",
            "provider": "Assigned Providers",
            "hist": "Patient History",
        }
        
class ProviderAdd(forms.ModelForm):
    class Meta:
        model = ProviderInfo
        fields = ('name','role','license_number','npi_number','dea_number')
        labels={"name":"Provider Full Name",
                'pid':'Provide a Provider ID for the Provider',
                "role":"Providers Titles (e.g. MD, LPN, etc.)",
                "license_number":"License Number",
                "npi_number":"NPI Number",}   

class AdministratorAdd(forms.ModelForm):
    class Meta:
        model = AdministratorInfo
        fields = ('name','role','license_number','npi_number')
        labels={"name":"Administrator Full Name",
                'pid':'Provide a Administrator ID for the Provider',
                "role":"Administrator Titles/Certifications",
                "license_number":"License Number",
                "npi_number":"NPI Number",}              
        
           

         
    