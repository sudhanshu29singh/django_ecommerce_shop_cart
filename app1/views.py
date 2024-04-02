from django.shortcuts import render,HttpResponse,redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required

from app1.models import Contact,Product,Orders
from math import ceil

from django.contrib import messages

# Create your views here.

@login_required(login_url='login')
def OrderPage(request):
    allProds = []
    catprods = Product.objects.values('category','id')
    cats = {item['category'] for item in catprods}
    for cat in cats:
        prod = Product.objects.filter(category=cat)
        n = len(prod)
        nSlides = n//4 + ceil((n/4)-(n//4))
        allProds.append([prod, range( 1, nSlides), nSlides])
    params = {'allProds':allProds}
    return render (request,'order.html',params)


def index(request):
    allProds = []
    catprods = Product.objects.values('category','id')
    cats = {item['category'] for item in catprods}
    for cat in cats:
        prod = Product.objects.filter(category=cat)
        n = len(prod)
        nSlides = n//4 + ceil((n/4)-(n//4))
        allProds.append([prod, range( 1, nSlides), nSlides])
    params = {'allProds':allProds}
    return render (request,'index.html',params)

def SignupPage(request):
    if request.method=='POST':
        uname=request.POST.get('username')
        email=request.POST.get('email')
        pass1=request.POST.get('password1')
        pass2=request.POST.get('password2')

        if pass1!=pass2:
            return HttpResponse("Your password and confrom password are not Same!!")
        else:

            my_user=User.objects.create_user(uname,email,pass1)
            my_user.save()
            return redirect('login')

    return render (request,'signup.html')

def LoginPage(request):
    if request.method=='POST':
        username=request.POST.get('username')
        pass1=request.POST.get('password1')
        user=authenticate(request,username=username,password=pass1)
        if user is not None:
            login(request,user)
            return redirect('order')
        else:
            messages.info(request, 'Account not found')
            # return HttpResponse ("Username or Password is incorrect!!!")

    return render (request,'login.html')

def LogoutPage(request):
    logout(request)
    return redirect('login')

def contact(request):
    if request.method=='POST':
        name = request.POST.get('name','')
        email = request.POST.get('email1','')
        phone = request.POST.get('phone','')
        desc = request.POST.get('desc','')
        print(name, email, phone, desc)
        contact = Contact(name=name, email=email, phone=phone, desc=desc)
        contact.save()
    return render(request,'contact.html')


def checkout(request):

    if request.method=="POST":
        items_json = request.POST.get('itemsJson', '')
        name = request.POST.get('name', '')
        # amount = request.POST.get('amt')
        email = request.POST.get('email', '')
        address1 = request.POST.get('address1', '')
        city = request.POST.get('city', '')
        state = request.POST.get('state', '')
        zip_code = request.POST.get('zip_code', '')
        phone = request.POST.get('phone', '')
        Order = Orders(items_json=items_json,name=name, email=email, address1=address1,city=city,state=state,zip_code=zip_code,phone=phone)
        # print(amount)
        Order.save()
        return render(request,'thankyou.html')
    return render(request, 'checkout.html')


def about(request):
    return render(request,'about.html')

@login_required(login_url='login')
def thankyou(request):
    return render(request,'thankyou.html')
