from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
]
urlpatterns += [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('departments/', views.departments, name='departments'),
    path('doctors/', views.doctors, name='doctors'),
    path('appointments/', views.appointments, name='appointments'),
    path('contact/', views.contact, name='contact'),
]