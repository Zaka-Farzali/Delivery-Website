
from django.contrib import admin
from django.urls import path
from deliveryapp import views 

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',views.home),
    path('aboutus/',views.aboutus),
    path('signin/', views.signin_user),
    path('signup/', views.signup_user),
]
