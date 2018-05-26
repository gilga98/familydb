from django.contrib import admin
from django.urls import path,include

from django.contrib.auth.views import logout
from . import views
app_name='chatbot'
urlpatterns=[
    path('',views.index,name='index'),
    path('login/',views.userlogin,name='login'),
    path('reg/',views.userreg,name='userreg'),
    path('logout/',views.ulogout,name="loguout")

]