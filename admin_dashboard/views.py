from django.shortcuts import render
from django.views import View

# Create your views here.
class AdminDashboardBase(View):
    def post(self, request):
        pass


    def get(self, request):
        return render(request, 'admin_dashboard_base.html')


class AdminDashboardHome(View):

    def post(self, request):
        pass


    def get(self, request):
        return render(request, 'admin_dashboard_home.html')