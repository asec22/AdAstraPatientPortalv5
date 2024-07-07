from django.urls import path
from . import views

# create your urls here
urlpatterns=[
    path("<str:name>/entervitals/",views.entervitals,name="entervitals"),
    path("<str:name>/entervisit/",views.entervisit,name="entervisit"),
    path("<str:name>/viewvitals/",views.viewvitals,name="viewvitals"),
    path("<str:name>/viewvisits/",views.viewvisits,name="viewvisits"),
    path("<str:name>/entercontact/",views.entercontact,name="entercontact"),
    path("<str:name>/enterecontact/",views.enteremergencycontact,name="enterecontact"),
    path("<str:name>/enterinsurance/",views.enterinsurance,name="enterpatcontact"),
    path("<str:name>/viewcontact/",views.viewcontact,name="viewcontact"),
    path("<str:name>/viewecontact/",views.viewecontact,name="viewecontact"),
    path("<str:name>/viewinsurance/",views.viewinsurance,name="viewinsurance"),
    path("<str:name>/patientsummary/",views.patientsummary,name="patientsummary"),
]        