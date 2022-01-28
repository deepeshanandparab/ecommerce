from ast import Not
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib import auth, messages
from .forms import RegistrationForm
from .models import Profile
import re
# from .forms import ProfileUpdateForm

def signup(request):
    regex = re.compile('[@_!#$%^&*()<>?/\|}{~:]')
    atr = '@'

    postdata = request.POST
    first_name = postdata.get('first_name')
    last_name = postdata.get('last_name')
    username = postdata.get('username')
    email = postdata.get('email')

    value = {
        'first_name': first_name,
        'last_name': last_name,
        'username': username,
        'email': email
    }


    if request.method == 'POST':
        form = RegistrationForm(request.POST)
    
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created sucessfully for {username}. You can login now.')
            return redirect('loginpage')
        elif request.POST['first_name'] == '':
            messages.error(request, 'First name field is empty')
        elif request.POST['last_name'] == '':
            messages.error(request, 'Last name field is empty')
        elif request.POST['username'] == '':
            messages.error(request, 'Username field is empty')
        elif regex.search(request.POST['username']) is not None:
            messages.error(request, 'Username cannot have special characters')
        elif request.POST['email'] == '':
            messages.error(request, 'Email field is empty')
        elif atr not in request.POST['email']:
            messages.error(request, 'Email is Invalid')
        elif request.POST['password1'] == '':
            messages.error(request, 'Password field is empty')
        elif request.POST['password1'] != request.POST['password2']:
            messages.error(request, 'Passwords do not match')
    else:
        form = RegistrationForm()
    context = {'form': form, 'title': 'Sign Up', 'value': value}
    return render(request, 'signup.html', context)


def login(request):
    if request.method == 'POST':
        user = auth.authenticate(username=request.POST['username'], password=request.POST['password'])
        if user is not None:
            request.session['username'] = request.POST['username']
            auth.login(request, user)
            return redirect('homepage')
        else:
            messages.error(request, 'Username or Password is incorrect!')
            return render(request, 'login.html', {'title':'Login'})
    else:
        return render(request, 'login.html', {'title':'Login'})


def logout(request):
        auth.logout(request)
        return redirect('homepage')


# @login_required
# def updateProfilePage(request, id):
#     profile = Profile.objects.get(user_id=id)
#     form = ProfileUpdateForm(request.POST or None, request.FILES or None, instance=profile)
#     if form.is_valid():
#         form.save()
#         messages.success(request, 'Profile has been updated successfully.')
#         return redirect('my_product_page')
#     context = {'title':'Profile Update', 'form':form}
#     return render(request, 'accounts/update_profile.html', context)






# Create your views here.
# def signup(request):
#     return render(request, 'signup.html')


def myart(request):
    return render(request, 'myart.html')


def profile(request):
    return render(request, 'profile.html')

