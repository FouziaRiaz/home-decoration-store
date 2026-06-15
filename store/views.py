from django.contrib.auth import authenticate,login,logout
from django.http import HttpResponse,HttpResponseRedirect
from django.urls import reverse
from django.db import IntegrityError
from django.shortcuts import render,get_object_or_404
from django.http import JsonResponse
import json
import datetime
from .models import *
from .utils import cookieCart,cartData,guestOrder                
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator                                                                    

# Create your views here.


def store(request, category_slug= None):
    categories = None
    products = None

    if category_slug != None:
        categories = get_object_or_404(Category, slug=category_slug)
        products=Product.objects.filter(category=categories)
        data = cartData(request)
        cartItems = data['cartItems']
        context={'products':products,'cartItems':cartItems, 'category': categories,}
        return render(request,'store/product.html',context)

    else:
        products=Product.objects.all().filter(is_available=True)
    paginator = Paginator(products,9) 
    page = request.GET.get('page')
    paged_products = paginator.get_page(page)
    data = cartData(request)
    cartItems = data['cartItems']
    categories = Category.objects.all()
    context={'products':paged_products,'cartItems':cartItems, 'category':categories}
    return render(request,'store/store.html',context)




def cart(request):
    data= cartData(request)
    cartItems= data['cartItems']
    order=data['order']
    items=data['items']

    return render(request,"store/cart.html",{"items":items,"order":order,"cartItems":cartItems})

def checkout(request):
    data= cartData(request)
    cartItems= data['cartItems']
    order=data['order']
    items=data['items']
    
    return render(request,"store/checkout.html",{"items":items,"order":order,"cartItems":cartItems})

def updateItem(request):
    data=json.loads(request.body)
    productId=data['productId']
    action=data['action']
    print('Action:',action)
    print('ProductId:',productId)

    customer=request.user.customer
    product = Product.objects.get(id=productId)
    order = Order.objects.filter(customer=customer,complete=False).first() # or .last() based on your requirements
    if not order:
        order = Order.objects.create(customer=customer,complete=False)
    orderItem, created = OrderItem.objects.get_or_create(order=order, product=product)
     
    if action =='add':
        orderItem.quantity=(orderItem.quantity + 1)
    elif action == 'remove':
        orderItem.quantity=(orderItem.quantity - 1)
    orderItem.save()

    if orderItem.quantity <=0:
        orderItem.delete()
    return JsonResponse('item was added',safe=False)

def processOrder(request):
    transaction_id=datetime.datetime.now().timestamp()
    data= json.loads(request.body)

    if request.user.is_authenticated:
        customer = request.user.customer
        order = Order.objects.filter(customer=customer,complete=False).first() # or .last() based on your requirements
        if not order:
            order = Order.objects.create(customer=customer,complete=False)
    else:
        customer,order= guestOrder(request,data)
    
    
    total = float(data['form']['total'])
    order.transaction_id=transaction_id

    # bcz we will be sending the total from the frontend, want to make sure that the total sent matches what the cart total is actually supposed to be:
    if total == float(order.get_cart_total):
        order.complete=True
    order.save()
    

    # Now we need to create an instance of the shipping address if an address was sent:
   
    ShippingAddress.objects.create(
        customer=customer,
        order=order,
        address=data['shipping']['address'],
        city=data['shipping']['city'],
        state=data['shipping']['state'],
        zipcode=data['shipping']['zipcode'],
    )
    return JsonResponse('Payment Complete!', safe=False)
def login_view(request):
    if request.method =='POST':
        username=request.POST["username"]
        password=request.POST["password"]
        user= authenticate(request,username=username,password=password)
        if user:
            login(request,user)
            return HttpResponseRedirect(reverse("cart"))
        else:
            return render(request, "store/login.html",{"message": "Invalid username and/or password."})
    else:
        return render(request, "store/login.html")

def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("store"))

def register(request):
    if request.method == 'POST':
        username=request.POST["username"]
        email=request.POST["email"]

        # ensure password matches confirmation
        password=request.POST["password"]
        confirmation=request.POST["confirmation"]
        if password != confirmation:
            return render(request,"store/login.html", {"message": "Passwords must match."})
        
        # Attempt to create a new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
            
        except IntegrityError:
            return render(request, "store/register.html",{
                "message": "Username already taken."
            })
        
        login(request,user)
        return HttpResponseRedirect(reverse("store"))
    else:
        return render(request,"store/register.html")



