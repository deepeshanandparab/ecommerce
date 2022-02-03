from django.shortcuts import render
from django.views import View
from store.models import User
from django.db.models import Count
import datetime
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db.models import Q

# Create your views here.
class AdminDashboardHome(View):

    def post(self, request):
        pass


    def get(self, request):
        context = {'page_title': 'Admin Dashboard Home'}
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
            print('first loop month', month)
            if (month < 1):
                month = 12
                year = today.year - 1
                while month > 0 and month != today.month:
                    monthly_list = User.objects.filter(date_joined__month=month,date_joined__year=year)
                    users_list.append(monthly_list)
                    month = month - 1
                    print('second loop month', month)
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




