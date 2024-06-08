from django.urls import path
from . import views

urlpatterns = [
    path('', views.RepairView.as_view(), name='repair'),
   
]
