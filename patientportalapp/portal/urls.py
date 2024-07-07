from django.urls import path
from . import views

urlpatterns=[
    path("",views.portal,name="portal"),
    path("createpat/",views.createpat,name="createpat"),
    path("createprov/",views.createprov,name="createpat"),
    path("createad/",views.createad,name="createad"),
    path("viewpatlist/",views.viewpatlist,name="viewpatlist"),
    path("viewprovlist/",views.viewprovlist,name="viewprovlist"),
    path("viewadlist/",views.viewadlist,name="viewadlist"),
    path("patient/<str:name>/",views.viewpatinfo,name="viewpatinfo"),
    path("provider/<str:name>/",views.viewprovinfo,name="viewpatinfo"),
    path("administrator/<str:name>/",views.viewadinfo,name="viewadinfo"),   
]