from django.urls import path
from . import views

urlpatterns = [
    path('profit/', views.EnterpriseProfit.as_view(), name='enterprise_profit'),
   
]
