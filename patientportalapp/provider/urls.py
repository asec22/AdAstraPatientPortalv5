from django.urls import path
from . import views

urlpatterns=[
    path("<str:name>/entercontact",views.entercontact,name="entercontact"),
    path("<str:name>/viewcontact",views.viewcontact,name="viewcontact"),
    path('<str:name>/entermedprescription/',views.entermedprescription,name='entermedprescription'),
    path('<str:name>/viewprescriptionlist/',views.viewprescriptionlist,name="viewprescriptionlist"),
    path('<str:name1>/<str:name2>/<str:med>/viewmedprescription/',views.viewmedprescription,name="viewmedprescription"),
    path('<str:name1>/<str:name2>/<str:med>/printmedprescription/',views.printmedprescription,name="printmedprescription"),
]

