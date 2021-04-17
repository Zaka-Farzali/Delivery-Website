
from django.contrib import admin
from django.urls import path
from deliveryapp import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home),
    path('aboutus/', views.aboutus, name='aboutus'),
    path('signin/', views.signin_user, name='sigin'),
    path('signup/', views.signup_user, name='signup'),
    path('signout/', views.signout_user, name='signout'),
    path('order/', views.order, name='order'),
    path('products/', views.products, name='products'),
    path('profile/', views.profile, name='profile'),
    path('deleteaccount/', views.deleteaccount, name='deleteaccount'),
    path('calculator/',views.calculator, name='calculator')
]
