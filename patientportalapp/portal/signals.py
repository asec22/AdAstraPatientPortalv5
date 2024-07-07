from django.db.models.signals import pre_save
from django.dispatch import receiver
from .models import PatientInfo, AdministratorInfo, ProviderInfo

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
