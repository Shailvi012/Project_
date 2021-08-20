from django.shortcuts import render,redirect
from django.http import HttpResponse
from .models import *
import smtplib
import random
from django.contrib import messages
from django.core.paginator import Paginator
from django.core import serializers
import razorpay
from django.views.decorators.csrf import csrf_exempt

# Create your views here.
def index(request):
    obj = Product.objects.all()
    slider = Product.objects.all()[:3]
    s1 = Slider.objects.all()
    return render(request,"index.html",{'file' : obj,'slider':slider,'s1':s1})

def category(request,id):
    obj = Product.objects.filter(cat_name_id=id)
    return render(request,"index.html",{'file' : obj})

def home(request):
    obj = Register.objects.all()
    return render(request,'home.html',{'data': obj})

def about(request):
    return render(request,'about.html')

def register(request):
    if request.method == "POST":
        name = request.POST['name']
        email = request.POST['email']
        number = request.POST['number']
        pass1 = request.POST['pass1']
        pass2 = request.POST['pass2']
        if pass1 == pass2:
            obj = Register(Name=name,Email=email,Mobile_number=number,Password=pass1)
            obj.save()
            s = smtplib.SMTP('smtp.gmail.com', 587)  
            s.starttls() 
            s.login("shailvigandhi2000@gmail.com", "selhit3023")
            otp = random.randint(0000,9999)
            request.session['otp'] = otp
            message = f'Your otp is {otp}'
            request.session['email'] = email
            s.sendmail("shailvigandhi2000@gmail.com", f'{email}', message)
            s.quit() 
            return redirect('verify_otp')
        else:
            return redirect('register')
    else:
        return render(request,'Register.html') 

def login(request):
    if request.method == "POST":
        email = request.POST['email']
        pass1 = request.POST['pass1']
        try:
            valid = Register.objects.get(Email=email)
            if valid.Password == pass1 and valid.boolean == True:
                request.session['user']=email
                return redirect('index')
            else:
                return redirect('login')
        except:
            return redirect('login')
    else:
        return render(request,'login.html')



def logout(request):
    if 'user' in request.session:
        del request.session['user']
        return redirect('login')
    return redirect('login')
    
def contact(request):
    if request.method == "POST":
        name = request.POST['name']
        number = request.POST['number']
        message = request.POST['message']
        obj = Contact(Name=name,Number=number,Message=message)
        obj.save()
        return redirect('index')
    else:
        return render(request,'contact.html')
    
def verify_otp(request):
    if request.method == "POST":
        otp = request.POST['otp']
        print(type(otp))
        print(type(request.session['otp']))
        if int(otp) == request.session['otp']:
            email = request.session['email']
            Register.objects.filter(Email=email).update(boolean = True)
            del request.session['otp']
            del request.session['email']
            return redirect(login)
        else :
            return redirect('verify_otp')
    else:
        return render(request,'verify_otp.html')

def add_to_cart(request,id):
    if 'user' in request.session:
        user = request.session['user']
        user = Register.objects.get(Email=user)
        count = Cart.objects.filter(User_id = user.id,Product_id=id).count()
        product = Product.objects.get(id=id)
        cart = Cart.objects.filter(User_id = user.id,Product_id=id)
        if count> 0:
            qty = cart[0].quntity +1
            price = qty*product.price
            Cart.objects.filter(User_id = user.id,Product_id=id).update(price =price,quntity = qty)
            return redirect('cart')
        else :
            crt = Cart(User_id = user.id,Product_id=id,price=product.price,quntity=1)
            crt.save() 
            return redirect('cart')
    else :
        return redirect('login')

def cart(request):
    if 'user' in request.session:
       
        user = request.session['user']
        user = Register.objects.get(Email=user)
        c1 = Cart.objects.filter(User_id = user.id)
        list1 = []
        for i in c1:
            list1.append(i.price)
        
        l1 = sum(list1)
        return render(request,'cart.html',{'c1':c1,'l1':l1})

    else :
        return redirect('login')

def checkout(request):
    if request.method == "POST":
        country  = request.POST['country']
        email  = request.POST['email']
        mobile  = request.POST['mobile']
        address = request.POST['address']
        user = request.session['user']
        user_info = Register.objects.get(Email=user)
        cart = Cart.objects.filter(User__id=user_info.id)
        for c in cart:
            obj=Order(User=user_info,cart=c, Country=country,Email=email,Mobile=mobile,Address=address)
            obj.save()
            c.status =True
            c.save()
        return redirect('payment')
    return render(request,'checkout.html')

def plus(request,id):
    cart= Cart.objects.filter(id = id)
    qty = cart[0].quntity +1
    price = qty*cart[0].Product.price
    Cart.objects.filter(id = id).update(price = price,quntity = qty)
    return redirect('cart')

def minus(request,id):
    cart = Cart.objects.filter(id = id)
    qty = cart[0].quntity - 1
    price = qty*cart[0].Product.price
    Cart.objects.filter(id = id).update(price = price,quntity = qty)
    return redirect('cart')

def delete(request,id):
    cart = Cart.objects.filter(id = id)
    cart.delete()
    return redirect('cart')

def order(request):
    user = request.session['user']
    data = Order.objects.filter(User__Email = user)
    return render(request,'order.html',{"data":data})

def payment(request):
    user = request.session['user']
    user = Register.objects.get(Email=user)
    c1 = Cart.objects.filter(User_id = user.id)
    list1 = []
    for i in c1:
        list1.append(i.price)
        
    l1 = sum(list1)
    amount = l1*100 #100 here means 1 dollar,1 rupree if currency INR
    client = razorpay.Client(auth=('rzp_test_CFejC5NTQ0NGvt','8VxIagZCwRP8eNs60Nq7Qxh7'))
    response = client.order.create({'amount':amount,'currency':'USD','payment_capture':1})
    print(response)
    context = {'response':response,'amount':amount}
    return render(request,"payment.html",context)

@csrf_exempt
def payment_success(request):
    if request.method =="POST":
        print(request.POST)
        return render(request,'payment_success.html')
    return redirect('/') 