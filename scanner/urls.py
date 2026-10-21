from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('api/scan/start/', views.start_scan_api, name='start_scan_api'),
    path('api/scan/status/<int:scan_id>/', views.scan_status_api, name='scan_status_api'),
    path('testbed/', views.vulnerable_testbed, name='vulnerable_testbed'),
]