from django.urls import path,include
from . import views

#define your urls here

urlpatterns=[
    path("",include("allauth.urls")),
    path("register/",views.register,name="register"),
    path('register/nosuccess/',views.nosuccess,name="nosuccess"),
    path('register/success/',views.success,name="success"),
]