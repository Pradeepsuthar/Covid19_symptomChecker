from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='Covid-19 Home Page'),
    path('check_symptom/', views.symptomChecker, name='Covid-19 Symptom Check'),
    path('check_symptom_tool/', views.symptomCheckerTool, name='Covid-19 Symptom Check Tool'),
    path('check_symptom_response/', views.symptomCheckerResponse, name='Covid-19 Symptom Check Response'),
    path('Statistics/', views.StatisticsMap, name='StatisticsMap'),
]