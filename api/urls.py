from django.urls import path

from . import views

urlpatterns = [
    path('scan', views.scan, name='scan'),
    path('read', views.read, name='read'),
    path('write', views.write, name='write'),
    path('sensor', views.sensor, name='sensor'),
]
