from django.db import models
import datetime
from django.utils import timezone
from portal.models import ProviderInfo
from phonenumber_field.modelfields import PhoneNumberField


# Create your models here.

class MedPrescription(models.Model):
    providerinfo=models.ForeignKey(ProviderInfo,on_delete=models.CASCADE,blank=True)
    pat_name=models.CharField(max_length=300)
    med_name=models.CharField(max_length=300)
    dose=models.CharField(max_length=300)
    supply=models.CharField(max_length=300)
    by=models.CharField(max_length=300)
    period=models.CharField(max_length=300)
    add_instructions=models.TextField(blank=True)
    dx_code=models.CharField(max_length=300)
    refill=models.IntegerField()
    label=models.BooleanField()
    generic=models.BooleanField()

    def __str__(self):
        return f"{self.pat_name}-{self.med_name}"

class ProvContactInfo(models.Model):
    providerinfo=models.ForeignKey(ProviderInfo, on_delete=models.CASCADE, blank=True)
    streetandnumber=models.CharField(max_length=300)
    city=models.CharField(max_length=300)
    state=models.CharField(max_length=300)
    zip=models.CharField(max_length=300)
    country=models.CharField(max_length=300)
    phone1=PhoneNumberField()
    phone2=PhoneNumberField(blank=True,null=True)
    email=models.EmailField(max_length=300,blank=True,null=True)
    
    def __str__(self):
        return f"{self.providerinfo}-{self.streetandnumber}"     

    


