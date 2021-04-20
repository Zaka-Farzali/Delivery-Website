from typing import OrderedDict
from django.http import response, JsonResponse
from django.db import IntegrityError
from django.shortcuts import redirect, render
from django.contrib.auth import get_user, login, logout, authenticate
from django.contrib.auth.hashers import make_password
from .models import Customer ,Order
import requests, json

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
        try:
            email = request.POST['email']
            name = request.POST['name']
            if name == "":
                return render(request,'signupuser.html' , context = {'response':response, 'error': 'Please enter your name'})
            surname = request.POST['surname']
            if surname == "":
                return render(request,'signupuser.html' , context = {'response':response, 'error': 'Please enter your surname'})
            phone = request.POST['phone']
            if phone == "":
                return render(request,'signupuser.html' , context = {'response':response, 'error': 'Please enter your phone number'})
            address = request.POST['address']
            if address == "":
                return render(request,'signupuser.html' , context = {'response':response, 'error': 'Please enter your address'})
            birthday = request.POST['birthday']
            if birthday == "":
                return render(request,'signupuser.html' , context = {'response':response, 'error': 'Please enter your birthday'})
            password1 = request.POST['password1']
            password2 = request.POST['password2']
            if password1 != password2:
                return render(request,'signupuser.html' , context = {'response':response, 'error': 'Passswords do not match. Please try again'})
            user = Customer.objects.create_user(email, name, surname, phone, address, birthday, password = password1)
            login(request,user)
            return redirect(home)
        except IntegrityError:
            return render(request,'signupuser.html' , context = {'response':response, 'error': 'User with this email already exists'})


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
        url = request.POST['link']
        if url == "":
            return render(request, 'order.html', context={'error': 'Please input the url of the product'})
        color = request.POST['color']
        size = request.POST['size']
        if size == "":
            return render(request, 'order.html', context={'error': 'Please input the size of the product'})
        amount = int(request.POST['amount'])
        if amount <=0:
            return render(request, 'order.html', context={'error': 'Please input the correct amount'})
        price = float(request.POST['price'])
        if price <=0:
             return render(request, 'order.html', context={'error': 'Please input the correct amount'}) 
        other = request.POST['other']
        order = {
            'url':url,
            'color':color,
            'size':size,
            'amount':amount,
            'price':(0.1*amount*price) + (amount*price),
            'other':other,
            }
        # customer = Order.objects.create(url=url, color= color, size = size, amount = amount, otherInfo = other, customer = get_user(request))
        return render(request, 'checkout.html', context={'order':order})

# def order_check(request):

def products(request):
    try:
        response = currencies()
        orderdict = Order.objects.filter(customer = get_user(request))
        return render(request, 'products.html', context={'response' : response, 'orderdict' : orderdict})
    except TypeError:
        return render(request, 'products.html', context={'response' : response})
        

def profile(request):
    if request.method == 'POST':
            u = Customer.objects.get(email = get_user(request))
            u.delete()
            return render(request, 'profile.html',context={'message':'Account is succesfully deleted'})
    else:
        user = Customer.objects.get(email = get_user(request))
        return render(request, 'profile.html',context={'user':user})

def deleteaccount(request):
    u = Customer.objects.get(email = get_user(request))
    u.delete()
    return render(request, 'profile.html',context={'message':'Account is succesfully deleted'})
    
def calculator(request):
    if request.method == 'GET':
        return render(request,'calculator.html')
    if request.method == 'POST':
        weight = request.POST['weight']
        length = request.POST['length']
        width = request.POST['width']
        height = request.POST['height']
        tmp = float(length+width+height)
        print(tmp)
        price = 6.99 + float(weight)*1.5 + (float(length)+float(width)+float(height))*0.2
        price = round(price,2)
        return render(request,'calculator.html', context={'price':price})

def checkout(request):
    return render(request, 'checkout.html')

def complete(request):
    order = json.loads(request.body)
    Order.objects.create(url=order['url'], color= order['color'], size = order['size'], amount = order['amount'], price = order['price'],otherInfo = order['other'], customer = get_user(request))
    return JsonResponse('Payment completed!', safe = False)