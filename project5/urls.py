"""project5 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from application5 import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('index',views.index,name ='index'),
    path('home',views.home,name ='home'),
    path('about',views.about,name ='about'),
    path('register',views.register,name ='register'),
    path('login',views.login,name ='login'),
    path('logout',views.logout,name ='logout'),
    path('category/<int:id>',views.category,name ='category'),
    path('contact',views.contact,name ='contact'),
    path('verify_otp',views.verify_otp,name ='verify_otp'),
    path('add_to_cart/<int:id>',views.add_to_cart,name ='add_to_cart'),
    path('cart',views.cart,name ='cart'),
    path('checkout',views.checkout,name ='checkout'),
    path('plus/<int:id>',views.plus,name ='plus'),
    path('minus/<int:id>',views.minus,name ='minus'),
    path('delete/<int:id>',views.delete,name ='delete'),
    path('order/',views.order,name ='order'),
    path('payment/',views.payment,name='payment'),
    path('success/',views.payment_success,name='success'),
]+ static(settings.MEDIA_URL,document_root = settings.MEDIA_ROOT) 
