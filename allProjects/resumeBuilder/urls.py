from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='Resume Home Page'),
    path('myresume/', views.showResume, name='Show my Resume'),
    path('edit/', views.editResume, name='Edit my Resume'),
]