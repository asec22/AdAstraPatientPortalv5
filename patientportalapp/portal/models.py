from django.db import models
from django.conf import settings
from django.utils import timezone
from phonenumber_field.modelfields import PhoneNumberField
import datetime
import pytz
import uuid
import random
from django.db.models.signals import pre_save
from django.dispatch import receiver

# Create your models here.

ROLES = [
    ('Doctor', 'Doctor'),
    ('Physician Assistant', 'Physician Assistant'),
    ('Nurse Practitioner', 'Nurse Practitioner'),
    ('Nurse', 'Nurse'),
    ('Nursing Aide', 'Nursing Aide'),
    ('Therapist', 'Therapist'),
    ('Technician', 'Technician'),
]

class ProviderInfo(models.Model):
    pid = models.CharField(max_length=300,editable=False,blank=True)
    role=models.CharField(max_length=300,choices=ROLES)
    name=models.CharField(max_length=300)
    license_number=models.CharField(max_length=300)
    npi_number=models.CharField(max_length=300)
    dea_number=models.CharField(max_length=300,blank=True)
    group=models.CharField(max_length=100,default="Provider",editable=False)

    def __str__(self):
        return self.name
    
class AdministratorInfo(models.Model):
    pid = models.CharField(max_length=300,editable=False, blank=True)
    role=models.CharField(max_length=300)
    name=models.CharField(max_length=300)
    license_number=models.CharField(max_length=300, blank=True , null=True)
    npi_number=models.CharField(max_length=300, blank=True, null=True)
    group=models.CharField(max_length=100, default="Administrator",editable=False)

    def __str__(self):
        return self.name  
    
class PatientInfo(models.Model):
    pid = models.CharField(max_length=300,editable=False, blank=True)
    name = models.CharField(max_length=300)
    bdate = models.DateField()
    age = models.IntegerField(editable=False, blank=True)
    gender = models.CharField(max_length=300)
    provider = models.ManyToManyField(ProviderInfo, blank=True)
    hist = models.TextField()
    group=models.CharField(max_length=100,default="Patient",editable=False)
    
    def __str__(self):
        return self.name
    
    class Meta:
        constraints = [
            models.CheckConstraint(check=models.Q(age__gte=0), name='age_non_negative'),
            ]
        
    @property
    def computed_age(self):
        today = datetime.date.today()
        age = today.year - self.bdate.year - ((today.month, today.day) < (self.bdate.month, self.bdate.day))
        return age
    
    def save(self, *args, **kwargs):
        self.age = self.computed_age
        super().save(*args, **kwargs)

def set_sequential_id(model_class, instance, prefix, **kwargs):
    if not instance.pid:
        last_instance = model_class.objects.order_by('-id').first()
        if last_instance:
            last_id = int(last_instance.pid[len(prefix):])  # Extract the numeric part of the last pid
            new_id = f'{prefix}{last_id + 1:05d}'  # Increment and format with leading zeros
        else:
            new_id = f'{prefix}00001'  # Starting value
        instance.pid = new_id

@receiver(pre_save, sender=PatientInfo)
def set_patinfo_pid(sender, instance, **kwargs):
    set_sequential_id(PatientInfo, instance, 'PT')

@receiver(pre_save, sender=AdministratorInfo)
def set_admininfo_pid(sender, instance, **kwargs):
    set_sequential_id(AdministratorInfo, instance, 'AD')

@receiver(pre_save, sender=ProviderInfo)
def set_providerinfo_pid(sender, instance, **kwargs):
    set_sequential_id(ProviderInfo, instance, 'PR')        

    
