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
from django.db.models import Sum
from django.http import JsonResponse


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


today = datetime.date.today()
month = today.month
seven_days = datetime.timedelta(7)
last_week = today - seven_days


class AdminDashboardOrderPending(View):

    def post(self, request):
        pass


    def get(self, request):
        this_day = request.GET.get('today')
        this_week = request.GET.get('this_week')
        this_month = request.GET.get('this_month')

        all_pending_order = Order.objects.filter(status='pending')
        orders_today = Order.objects.filter(date=today)
        orders_this_week = Order.objects.filter(date__gte=last_week)
        orders_this_month = Order.objects.filter(date__month=month)

        if this_day == 'clicked':
            pending_order_list = all_pending_order.intersection(orders_today).order_by('-date')
        elif this_week == 'clicked':
            pending_order_list = all_pending_order.intersection(orders_this_week).order_by('-date')
        elif this_month == 'clicked':
            pending_order_list = all_pending_order.intersection(orders_this_month).order_by('-date')
        else:
            pending_order_list = all_pending_order.intersection(orders_today).order_by('-date')


        paginator = Paginator(pending_order_list, 10)
        page = request.GET.get('page')
        try:
            response = paginator.page(page)
        except PageNotAnInteger:
            response = paginator.page(1)
        except EmptyPage:
            response = paginator.page(paginator.num_pages)

        first_item_number = 10 * (response.number - 1) + 1
        context = {
                    'pending_order_list': response,
                    'page_size': 10,
                    'page_number': page,
                    'first_item_number': first_item_number,
                    'today': today
                    }
        return render(request, 'admin_dashboard_orders_pending.html', context)


class AdminDashboardOrderComplete(View):

    def post(self, request):
        pass


    def get(self, request):
        this_day = request.GET.get('today')
        this_week = request.GET.get('this_week')
        this_month = request.GET.get('this_month')
        
        all_complete_order = Order.objects.filter(status='complete')
        orders_today = Order.objects.filter(date=today)
        orders_this_week = Order.objects.filter(date__gte=last_week)
        print('orders_this_week', orders_this_week)
        orders_this_month = Order.objects.filter(date__month=month)

        if this_day == 'clicked':
            complete_order_list = all_complete_order.intersection(orders_today).order_by('-date')
        elif this_week == 'clicked':
            complete_order_list = all_complete_order.intersection(orders_this_week).order_by('-date')
        elif this_month == 'clicked':
            complete_order_list = all_complete_order.intersection(orders_this_month).order_by('-date')
        else:
            complete_order_list = all_complete_order.intersection(orders_today).order_by('-date')


        paginator = Paginator(complete_order_list, 10)
        page = request.GET.get('page')
        try:
            response = paginator.page(page)
        except PageNotAnInteger:
            response = paginator.page(1)
        except EmptyPage:
            response = paginator.page(paginator.num_pages)

        first_item_number = 10 * (response.number - 1) + 1
        context = {
                    'complete_order_list': response,
                    'page_size': 10,
                    'page_number': page,
                    'first_item_number': first_item_number,
                    'today': today
                    }
        return render(request, 'admin_dashboard_orders_complete.html', context)



class AdminDashboardOrderCancelled(View):

    def post(self, request):
        pass


    def get(self, request):
        this_day = request.GET.get('today')
        this_week = request.GET.get('this_week')
        this_month = request.GET.get('this_month')
        
        all_cancelled_order = Order.objects.filter(status='cancelled')
        orders_today = Order.objects.filter(date=today)
        orders_this_week = Order.objects.filter(date__gte=last_week)
        orders_this_month = Order.objects.filter(date__month=month)

        if this_day == 'clicked':
            cancelled_order_list = all_cancelled_order.intersection(orders_today).order_by('-date')
        elif this_week == 'clicked':
            cancelled_order_list = all_cancelled_order.intersection(orders_this_week).order_by('-date')
        elif this_month == 'clicked':
            cancelled_order_list = all_cancelled_order.intersection(orders_this_month).order_by('-date')
        else:
            cancelled_order_list = all_cancelled_order.intersection(orders_today).order_by('-date')


        paginator = Paginator(cancelled_order_list, 10)
        page = request.GET.get('page')
        try:
            response = paginator.page(page)
        except PageNotAnInteger:
            response = paginator.page(1)
        except EmptyPage:
            response = paginator.page(paginator.num_pages)

        first_item_number = 10 * (response.number - 1) + 1
        context = {
                    'cancelled_order_list': response,
                    'page_size': 10,
                    'page_number': page,
                    'first_item_number': first_item_number,
                    'today': today
                    }
        return render(request, 'admin_dashboard_orders_cancelled.html', context)




class AdminDashboardSale(View):

    def post(self, request):
        pass


    def get(self, request):
        products_type_list = []
        temp_list = []
        art_type = ProductType.objects.all()

        for type in art_type:
            product_list = Product.objects.filter(art_type=type.value)
            sold_list = Product.objects.filter(sold_quantity__gt=0)
            temp_list = product_list.intersection(sold_list)

            products_type_list.append(temp_list) 
            

        top_selling_products_list = Product.objects.filter(sold_quantity__gt=0).order_by('-sold_quantity')[:5]

        labels = []
        data = []

        order_list = Order.objects.order_by('-date')[:5]
        for order in order_list:
            labels.append(order.date)
            data.append(order.price)

        orders_price_list = Order.objects.filter(date__month=month).order_by('-date')
        selling_price_sum = 0
        for sales in orders_price_list:
            selling_price_sum = selling_price_sum + sales.price
        monthly_sales = selling_price_sum


        buying_price_sum = 0
        for buy in orders_price_list:
            buying_price_sum = buying_price_sum + buy.product.buyingprice_set.values('buying_price')[0].get('buying_price')
        buying_price = buying_price_sum

        revenue = monthly_sales - buying_price


        context = {
                    'top_selling_products_list': top_selling_products_list,
                    'products_type_list': products_type_list,
                    'labels': labels,
                    'data': data,
                    'monthly_sales': monthly_sales,
                    'today': today,
                    'revenue': revenue
        }
        return render(request, 'admin_dashboard_sale.html', context)



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

def MarkOrderComplete(request, id):
    if request.method == 'POST':
        order = Order.objects.get(id=id)
        Order.objects.filter(id=id).update(status = 'complete')
        messages.success(request, f'Order - {order.order_id} Marked as Complete')

    return redirect('admindashboardordercompletepage')


def SalesChart(request):
    labels = []
    data = []

    queryset = Order.objects.values('date').filter(date__month=month).annotate(daily_sale=Sum('price')).order_by('-date')

    for entry in queryset:
        labels.append(entry['date'])
        data.append(entry['daily_sale'])
    
    return JsonResponse(data={
        'labels': labels,
        'data': data,
    })






