
from django.contrib import admin
from django.urls import path
from deliveryapp import views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home),
    path('home/', views.home),
    path('aboutus/', views.aboutus, name='aboutus'),
    path('signin/', views.signin_user, name='sigin'),
    path('signup/', views.signup_user, name='signup'),
    path('signout/', views.signout_user, name='signout'),
    path('order/', views.order, name='order'),
    path('products/', views.products, name='products'),
    path('profile/', views.profile, name='profile'),
    path('deleteaccount/', views.deleteaccount, name='deleteaccount'),
    path('calculator/',views.calculator, name='calculator'),
    path('checkout/',views.checkout, name='checkout'),
    path('complete/',views.complete, name='complete'),
    path('partners/', views.partners, name='partners')

]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
