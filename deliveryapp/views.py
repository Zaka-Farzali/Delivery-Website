from django.http import response
from django.shortcuts import render
import requests
# Create your views here.


def home(request):
    response1 = requests.get('https://api.exchangeratesapi.io/latest?base=USD')
    response2= requests.get('https://api.exchangeratesapi.io/latest?base=EUR')
    response3 = requests.get('https://api.exchangeratesapi.io/latest?base=TRY')
    response1 = response1.json()
    response2 = response2.json()
    response3 = response3.json()
    response = {"EUR": round(response1['rates']['HUF'],4),
                "USD": round(response2['rates']['HUF'],4),
                "TRY": round(response3['rates']['HUF'],4),
               }
    return(render(request,'home.html', context = {'response':response}))

def aboutus(request):
    response1 = requests.get('https://api.exchangeratesapi.io/latest?base=USD')
    response2= requests.get('https://api.exchangeratesapi.io/latest?base=EUR')
    response3 = requests.get('https://api.exchangeratesapi.io/latest?base=TRY')
    response1 = response1.json()
    response2 = response2.json()
    response3 = response3.json()
    response = {"EUR": round(response1['rates']['HUF'],4),
                "USD": round(response2['rates']['HUF'],4),
                "TRY": round(response3['rates']['HUF'],4),
               }
    return(render(request,'aboutus.html', context = {'response':response}))
