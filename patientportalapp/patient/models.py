from django.db import models
from portal.models import PatientInfo
from django.utils import timezone
from phonenumber_field.modelfields import PhoneNumberField
import datetime
import pytz
import uuid
import random

# Create your models here.

class Vitals(models.Model):
    patinfo=models.ForeignKey(PatientInfo, on_delete=models.CASCADE, blank=True)
    time=models.DateTimeField(default=timezone.now,blank=True, null=True)
    height=models.CharField(max_length=100)
    weight=models.FloatField()
    temperature=models.FloatField()
    resp_rate=models.IntegerField()
    pulse=models.IntegerField()
    oxy_sat=models.FloatField()
    blood_pressure=models.CharField(max_length=100)
    
    def __str__(self):
        our_tz = pytz.timezone('America/New_York')  
        return self.time.astimezone(our_tz).strftime('%B %d, %Y at %I:%M %p')
        
    @property
    def height_inch(self):
        h=self.height.split("-",1)
        hinch=(int(h[0])*12)+int(h[1])
        return hinch 
    
    @property
    def blood_pres(self):
        b=self.blood_pressure.split("/",1)
        bs=int(b[0])
        bd=int(b[1])
        bl=[bs,bd]
        return bl 
    
    @property
    def bmi(self):
        bmi=(float(self.weight)/((float(self.height_inch))**2))*703
        return bmi 

    @property
    def height_cm(self):
        hcm=float(self.height_inch)*2.54
        return hcm

    @property
    def weight_kg(self):
        wkg=float(self.weight)*0.4536
        return wkg

    @property
    def temp_cel(self):
        tcel=(float(self.temperature)-32)*(5/9)
        return tcel    
    
class Visit(models.Model):
    patinfo=models.ForeignKey(PatientInfo, on_delete=models.CASCADE, blank=True)
    time=models.DateTimeField(default=timezone.now, blank=True, null=True)
    reason=models.TextField()
    dx=models.TextField()
    px=models.TextField()
    lx=models.TextField()
    prx=models.TextField()
    patinst=models.TextField()
    
    def __str__(self):
        our_tz = pytz.timezone('America/New_York')  
        return self.time.astimezone(our_tz).strftime('%B %d, %Y at %I:%M %p')
        
class ContactInfo(models.Model):
    patinfo=models.ForeignKey(PatientInfo, on_delete=models.CASCADE, blank=True)
    streetandnumber=models.CharField(max_length=300)
    city=models.CharField(max_length=300)
    state=models.CharField(max_length=300)
    zip=models.CharField(max_length=300)
    country=models.CharField(max_length=300)
    phone1=PhoneNumberField()
    phone2=PhoneNumberField(blank=True,null=True)
    email=models.EmailField(max_length=300,blank=True,null=True)
    
    def __str__(self):
        return f"{self.patinfo}-{self.streetandnumber}" 

class EmergencyContact(models.Model):
    patinfo=models.ForeignKey(PatientInfo, on_delete=models.CASCADE, blank=True)
    emergency_contact=models.CharField(max_length=300)
    relation=models.CharField(max_length=300)
    streetandnumber=models.CharField(max_length=300, blank=True, null=True)
    city=models.CharField(max_length=300, blank=True, null=True)
    state=models.CharField(max_length=300, blank=True, null=True)
    zip=models.CharField(max_length=300, blank=True, null=True)
    country=models.CharField(max_length=300,blank=True,null=True)
    phone1=PhoneNumberField()
    phone2=PhoneNumberField(blank=True,null=True)
    email=models.EmailField(max_length=300, blank=True, null=True)           

    def __str__(self):
        return self.emergency_contact
    
class InsuranceInfo(models.Model):
    patinfo=models.ForeignKey(PatientInfo, on_delete=models.CASCADE, blank=True)
    insurance_company=models.CharField(max_length=300)
    groupandnumber=models.CharField(max_length=300)
    streetandnumber=models.CharField(max_length=300)
    city=models.CharField(max_length=300)
    state=models.CharField(max_length=300)
    zip=models.CharField(max_length=300)
    country=models.CharField(max_length=300)
    phone=PhoneNumberField()
    fax=PhoneNumberField( blank=True, null=True)
    email=models.EmailField(max_length=300, blank=True, null=True)           

    def __str__(self):
        return self.insurance_company    