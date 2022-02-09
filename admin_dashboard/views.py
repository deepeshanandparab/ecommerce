import re
from django.shortcuts import redirect, render
from django.views import View
from store.models import Product, ProductType, User, Order, ImageAlbum, ProductCategory
from django.db.models import Count
import datetime
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db.models import Q
from django.contrib import messages
from .supporting_functions import generate_custom_string, get_sale_count, get_previous_month, get_product_category


# Create your views here.
class AdminDashboardHome(View):

    def post(self, request):
        pass


    def get(self, request):
        today = datetime.date.today()
        month = today.month
        top_selling_products_list = Product.objects.filter(sold_quantity__gt=0).order_by('-sold_quantity')[:5]
        orders_list = Order.objects.filter(date__month=month).order_by('-date')
        products_list = Product.objects.filter(discount__gte=10).order_by('-discount')
        users_list = User.objects.filter(date_joined__month=month)

        context = {'page_title': 'Admin Dashboard Home',
                    'top_selling_products_list': top_selling_products_list,
                    'orders_list':orders_list,
                    'products_list':products_list,
                    'users_list':users_list,
                    'sales_count':get_sale_count(month),
                    'previous_month': get_previous_month()}
        return render(request, 'admin_dashboard_home.html', context)


class AdminDashboardUser(View):

    def post(self, request):
        pass


    def get(self, request):
        users_list = []
        today = datetime.date.today()
        month = today.month
        while month > 0:
            monthly_list = User.objects.filter(date_joined__month=month,date_joined__year=today.year)
            users_list.append(monthly_list)
            month = month - 1
            if (month < 1):
                month = 12
                year = today.year - 1
                while month > 0 and month != today.month:
                    monthly_list = User.objects.filter(date_joined__month=month,date_joined__year=year)
                    users_list.append(monthly_list)
                    month = month - 1
                break


        # list = [
        #     [{'1A':'1A', '2A':'2A','3A':'3A'},{'1A':'1B', '2A':'2B','3A':'3B'}],
        #     [{'1A':'1A', '2A':'2A','3A':'3A'},{'1A':'1B', '2A':'2B','3A':'3B'}],
        # ]
        context = {'users_list':users_list}
        return render(request, 'admin_dashboard_user.html', context)


class AdminDashboardAllUser(View):

    def post(self, request):
        pass


    def get(self, request):
        keyword = request.GET.get('name')

        if keyword != None:
            users_list = User.objects.filter(Q(first_name__contains=keyword)|
            Q(last_name__contains=keyword)).order_by('-date_joined')
        else:
            users_list = User.objects.filter(first_name__contains='').order_by('-date_joined')

        paginator = Paginator(users_list, 3)
        page = request.GET.get('page')
        try:
            response = paginator.page(page)
        except PageNotAnInteger:
            response = paginator.page(1)
        except EmptyPage:
            response = paginator.page(paginator.num_pages)

        first_item_number = 3 * (response.number - 1) + 1
        context = {
                    'users_list':response,
                    'search_filter': users_list,
                    'page_size': 3,
                    'page_number': page,
                    'first_item_number': first_item_number,
                    'search_keyword': keyword,
                }
        return render(request, 'admin_dashboard_all_user.html', context)


class AdminDashboardUserProfile(View):

    def post(self, request):
        pass


    def get(self, request, id):
         user = User.objects.get(id=id)
         pending_order_list = Order.objects.filter(user_id=id, status='pending')
         complete_order_list = Order.objects.filter(user_id=id, status='complete')
         context = {
                    'user':user, 
                    'pending_order_list': pending_order_list,
                    'complete_order_list': complete_order_list,
                    }
         return render(request, 'admin_dashboard_user_profile.html', context)


class AdminDashboardProduct(View):

    def post(self, request):
        name = request.POST.get('product_name')
        description = request.POST.get('product_description')
        price = request.POST.get('product_price')
        art_type = request.POST.get('product_art_type')
        artist = request.POST.get('product_artist')
        user = User.objects.get(username=artist)
        sold_by = request.POST.get('product_sold_by')
        discount = request.POST.get('product_discount')
        art_category = request.POST.get('product_art_category')
        original_by = request.POST.get('product_original_by')
        stock = request.POST.get('product_stock')
        product_image = request.POST.get('product_image')

        product = Product(
            name = name,
            description = description,
            price = price,
            art_type = art_type,
            artist = user,
            sold_by = sold_by,
            discount = discount,
            discounted_price = int(price) * (1 - int(discount)/100),
            art_category = art_category,
            original_art_by = original_by,
            stock_quantity = stock,
            approved = True,
            sku = generate_custom_string(name, art_type, art_category)
        )

        product.save()
        messages.success(request, 'New Product Added Successfully')
        return redirect('admindashboardproductpage')


    def get(self, request):
        id = request.GET.get('id')
        product = []
        if id != None:
            product = Product.objects.get(id=id)
        
        products_type_list = []
        art_type = ProductType.objects.all()

        for type in art_type:
            products_list = Product.objects.filter(art_type=type.value)
            products_type_list.append(products_list)
        
        users_list = User.objects.all()
        product_type_list = ProductType.objects.all()
        product_category_list = get_product_category(product_type_list)
        
        context = {'products_type_list': products_type_list,
                    'product':product,
                    'users_list': users_list,
                    'product_category_list': product_category_list,
                    'product_type_list':product_type_list}
        return render(request, 'admin_dashboard_product.html', context)


class AdminDashboardOrder(View):

    def post(self, request):
        pass


    def get(self, request):
        return render(request, 'admin_dashboard_order.html')


class AdminDashboardSale(View):

    def post(self, request):
        pass


    def get(self, request):
        return render(request, 'admin_dashboard_sale.html')



def AddNewProductType(request):
    if request.method == 'POST':
        type = request.POST.get('product_type')
        value = request.POST.get('product_type_value')

        product_type = ProductType(
            type = type,
            value = value
        )
        product_type.save()
        messages.success(request, f'New Product Type - {type} Added Successfully')

    return redirect('admindashboardproductpage')


def AddNewProductCategory(request):
    if request.method == 'POST':
        product_type_id = request.POST.get('type_value')
        type = ProductType.objects.get(id=product_type_id)
        category = request.POST.get('type_category').title()
        value = request.POST.get('type_category').lower()

        product_category = ProductCategory(
            type = type,
            category = category,
            value = value
        )
        product_category.save()
        messages.success(request, f'New Category - {category} Added Successfully')
    return redirect('admindashboardproductpage')


def UpdateProductCategory(request, id):
    if request.method == 'POST':
        product_category = ProductCategory.objects.get(id=id)
        category = request.POST.get('form_category').title()
        value = request.POST.get('form_category_value').lower()
        ProductCategory.objects.filter(id=id).update(category = category, value = value)
        messages.success(request, f'Product Category - {product_category.category} Updated Successfully')

    return redirect('admindashboardproductpage')


def DeleteProductCategory(request, id):
    if request.method == 'POST':
        product_category = ProductCategory.objects.get(id=id)
        ProductCategory.objects.get(id=id).delete()
        messages.success(request, f'Product Category - {product_category.category} Deleted Successfully')

    return redirect('admindashboardproductpage')


def DeleteProductType(request, id):
    if request.method == 'POST':
        product_type = ProductType.objects.get(id=id)
        ProductType.objects.get(id=id).delete()
        messages.success(request, f'Product Type - {product_type.type} Deleted Successfully')

    return redirect('admindashboardproductpage')





