from django.urls import path
from .views import AdminDashboardHome, AdminDashboardUser, AdminDashboardAllUser, AdminDashboardProduct, \
                            AdminDashboardOrder, AdminDashboardSale

urlpatterns = [
    path('', AdminDashboardHome.as_view(), name='admindashboardhomepage'),
    path('users', AdminDashboardUser.as_view(), name='admindashboarduserpage'),
    path('users/all-users', AdminDashboardAllUser.as_view(), name='admindashboardalluserpage'),
    path('products', AdminDashboardProduct.as_view(), name='admindashboardproductpage'),
    path('orders', AdminDashboardOrder.as_view(), name='admindashboardorderpage'),
    path('sales', AdminDashboardSale.as_view(), name='admindashboardsalepage'),
]
