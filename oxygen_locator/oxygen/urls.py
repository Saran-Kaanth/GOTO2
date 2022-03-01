from django.urls import path,include
from .views import *
from . import views
from django.contrib import admin
from django import urls
from django.contrib.auth.views import LoginView,LogoutView

urlpatterns=[
    path('',oxygen,name='oxygen'),
    path('result/',result,name="result"),
    path('signup/',signup,name="signup"),
    path('hospital/',HospitalView,name="hospital"),
    path('loaddata/',loaddata,name="loaddata"),
]

# path('home/',home,name='home'),