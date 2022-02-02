from django.urls import path
from .views import AdminDashboardHome, AdminDashboardBase

urlpatterns = [
    path('base', AdminDashboardBase.as_view(), name='admindashboardbasepage'),
    path('', AdminDashboardHome.as_view(), name='admindashboardhomepage')
]
