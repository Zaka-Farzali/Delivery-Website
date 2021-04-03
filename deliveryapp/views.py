from typing import OrderedDict
from django.http import response
from django.shortcuts import redirect, render
from django.contrib.auth import get_user, login, logout, authenticate
from django.contrib.auth.hashers import make_password
from .models import Customer ,Order
import requests
# Create your views here.
def currencies():
    response1 = requests.get('https://free.currconv.com/api/v7/convert?q=EUR_HUF&compact=ultra&apiKey=8dcdf450f8ec388d7100')
    response2= requests.get('https://free.currconv.com/api/v7/convert?q=USD_HUF&compact=ultra&apiKey=8dcdf450f8ec388d7100')
    response3 = requests.get('https://free.currconv.com/api/v7/convert?q=TRY_HUF&compact=ultra&apiKey=8dcdf450f8ec388d7100')
    response1 = response1.json()
    # print(response1)
    response2 = response2.json()
    response3 = response3.json()
    response = {} 
    # {"EUR": round(response1['EUR_HUF'],2),
    #             "USD": round(response2['USD_HUF'],2),
    #             "TRY": round(response3['TRY_HUF'],2),
    #            }
    return response



def home(request):
    response = currencies();
    return render(request,'home.html', context = {'response':response})

def aboutus(request):
    response = currencies();
    return render(request,'aboutus.html', context = {'response':response})

def signout_user(request):
    logout(request)
    return redirect(home)

def signup_user(request):
    response = currencies();
    if request.method == 'GET':
        return render(request,'signupuser.html' , context = {'response':response})
    if request.method == 'POST':
        user = Customer.objects.create_user(request.POST['email'], request.POST['name'], request.POST['surname'], request.POST['phone'], request.POST['address'], request.POST['birthday'], password = request.POST['password1'])
        login(request,user)
        return redirect(home)                                                       

def signin_user(request):
    response = currencies();
    if request.method == 'GET':
        return render(request,'signinuser.html', context = {'response':response})
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        
        if email == "":
            return render(request,'signinuser.html', context = {'response':response, 'error': "Please enter your email" })
        
        if password == "":
            return render(request,'signinuser.html', context = {'response':response, 'error': "Please enter your password" })
        
        user = authenticate(request, email = email, password = password)
        if user is None:
            return render(request,'signinuser.html', context = {'response':response, 'error': "Account does not exist, sign up first!" })
        login(request,user)
        return redirect(home)

def order(request):
    response = currencies()
    if request.method == 'GET':
        return render(request, 'order.html', context = {'response':response})
    if request.method == 'POST':
        link = request.POST['link']
        color = request.POST['color']
        size = request.POST['size']
        amount = request.POST['amount']
        other = request.POST['other']

        customer = Order.objects.create(url=link, color= color, size = size, amount = amount, otherInfo = other, customer = get_user(request))
        return render(request, 'order.html', context = {'response':response})

def products(request):
    orderdict = Order.objects.get(customer = get_user(request))
    
    return render(request, 'products.html', context={'orderdict' : orderdict})