from unicodedata import name
from django.urls import path
from .views import AdminDashboardHome, AdminDashboardUser, AdminDashboardAllUser, AdminDashboardProduct, \
                            AdminDashboardUserProfile, AdminDashboardOrder, AdminDashboardSale, \
                            AddNewProductType, DeleteProductType, AddNewProductCategory, DeleteProductCategory, \
                            UpdateProductCategory
urlpatterns = [
    path('', AdminDashboardHome.as_view(), name='admindashboardhomepage'),
    path('users', AdminDashboardUser.as_view(), name='admindashboarduserpage'),
    path('user/profile/<id>', AdminDashboardUserProfile.as_view(), name='admindashboarduserprofilepage'),
    path('users/all-users', AdminDashboardAllUser.as_view(), name='admindashboardalluserpage'),
    path('products', AdminDashboardProduct.as_view(), name='admindashboardproductpage'),
    path('orders', AdminDashboardOrder.as_view(), name='admindashboardorderpage'),
    path('sales', AdminDashboardSale.as_view(), name='admindashboardsalepage'),
    path('addnewproducttype', AddNewProductType, name='addnewproducttype'),
    path('deleteproducttype/<id>', DeleteProductType, name='deleteproducttype'),
    path('addnewproductcategory', AddNewProductCategory, name='addnewproductcategory'),
    path('deleteproductcategory/<id>', DeleteProductCategory, name='deleteproductcategory'),
    path('updateproductcategory/<id>', UpdateProductCategory, name='updateproductcategory')
]
