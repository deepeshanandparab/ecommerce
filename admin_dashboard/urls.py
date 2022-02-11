from unicodedata import name
from django.urls import path
from .views import AdminDashboardHome, AdminDashboardUser, AdminDashboardAllUser, AdminDashboardProduct, \
                            AdminDashboardUserProfile, AdminDashboardSale, \
                            AddNewProductType, DeleteProductType, AddNewProductCategory, DeleteProductCategory, \
                            UpdateProductCategory, MarkOrderComplete, AdminDashboardOrderPending, AdminDashboardOrderComplete, \
                            AdminDashboardOrderCancelled, SalesChart

urlpatterns = [
    path('', AdminDashboardHome.as_view(), name='admindashboardhomepage'),
    path('users', AdminDashboardUser.as_view(), name='admindashboarduserpage'),
    path('user/profile/<id>', AdminDashboardUserProfile.as_view(), name='admindashboarduserprofilepage'),
    path('users/all-users', AdminDashboardAllUser.as_view(), name='admindashboardalluserpage'),
    
    path('orders-pending', AdminDashboardOrderPending.as_view(), name='admindashboardorderpendingpage'),
    path('orders-complete', AdminDashboardOrderComplete.as_view(), name='admindashboardordercompletepage'),
    path('orders-cancelled', AdminDashboardOrderCancelled.as_view(), name='admindashboardordercancelpage'),
    path('markordercomplete/<id>', MarkOrderComplete, name='markordercomplete'),


    path('sales', AdminDashboardSale.as_view(), name='admindashboardsalepage'),

    path('products', AdminDashboardProduct.as_view(), name='admindashboardproductpage'),
    path('addnewproducttype', AddNewProductType, name='addnewproducttype'),
    path('deleteproducttype/<id>', DeleteProductType, name='deleteproducttype'),
    path('addnewproductcategory', AddNewProductCategory, name='addnewproductcategory'),
    path('deleteproductcategory/<id>', DeleteProductCategory, name='deleteproductcategory'),
    path('updateproductcategory/<id>', UpdateProductCategory, name='updateproductcategory'),

    path('sales-chart/', SalesChart, name='sales-chart'),
]