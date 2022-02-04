from django.shortcuts import render
from django.views import View
from store.models import Product, User, Order
from django.db.models import Count
import datetime
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db.models import Q
from .supporting_functions import generate_product_sku, get_sale_count, get_previous_month


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
        pass


    def get(self, request):
        return render(request, 'admin_dashboard_product.html')


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




