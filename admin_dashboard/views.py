from django.shortcuts import render
from django.views import View
from store.models import User
from django.db.models import Count
import datetime

# Create your views here.
class AdminDashboardHome(View):

    def post(self, request):
        pass


    def get(self, request):
        return render(request, 'admin_dashboard_home.html')


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

        # list = [
        #     [{'1A':'1A', '2A':'2A','3A':'3A'},{'1A':'1B', '2A':'2B','3A':'3B'}],
        #     [{'1A':'1A', '2A':'2A','3A':'3A'},{'1A':'1B', '2A':'2B','3A':'3B'}],
        # ]
        context = {'users_list':users_list}
        return render(request, 'admin_dashboard_user.html', context)


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




