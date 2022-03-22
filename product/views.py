from django.shortcuts import render , HttpResponse,get_object_or_404
from .models import *
from .form import *
# Create your views here.
from django.shortcuts import render,redirect,HttpResponseRedirect
from .form import LoginForm
from django.contrib.auth import authenticate,login ,logout
from order.models import *
from django.contrib import messages
from django.core.paginator import Paginator,EmptyPage,PageNotAnInteger


def order(request):
    category = Category.objects.all()
    current_user = request.user
    orders = Order.objects.filter(user_id=current_user.id)
    return render(request,'order_details.html',{'category':category,'orders':orders})

def order_detail(request,id):
    category = Category.objects.all()
    current_user = request.user
    order = Order.objects.get(user_id=current_user.id,id=id)
    orderitems = OrderProduct.objects.filter(order_id=id)
    return render(request,'order_details_id.html',{'category':category,'order':order,'orderitems':orderitems})


def index(request):
    current_user = request.user
    category = Category.objects.all()
    product = Product.objects.all()
    images = Images.objects.all()
    dayproducts = Product.objects.all()[:3]
    lastproducts = Product.objects.all().order_by('-id')[:3]
    randomproducts = Product.objects.all().order_by('?')[:3]
    request.session['cart_items'] = ShopCart.objects.filter(user_id=current_user.id).count()
    return render(request,'index.html',{'category':category,'product':product,'images':images,'dayproducts':dayproducts,'lastproducts':lastproducts,'randomproducts':randomproducts})

def category_products(request,id,slug):
    category = Category.objects.all()
    items = Product.objects.filter(category_id=id)
    paginator = Paginator(items,3)
    page = request.GET.get('page')
    try:
        products = paginator.page(page)
    except PageNotAnInteger:
        products = paginator.page(1)
    except EmptyPage:
        products = paginator.page(paginator.num_pages)
    return render(request,'products.html',{'category':category,'products':products})


def product_search(request):
    if request.method == 'POST':
        form = SearchForm(request.POST)
        if form.is_valid():
            category= Category.objects.all()
            query = form.cleaned_data['query']
            products = Product.objects.filter(title__contains=query)
            return render(request,'products_search.html',{'products':products,'category':category})
    return render(request, 'products_search.html')


def log(request):
    form = LoginForm(request.POST or None)
    if form.is_valid():
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password')
        user = authenticate(username=username,password=password)
        if user is not None:
            login(request,user)
            return redirect('/')
    return render(request,'login.html',{'form' : form})

def logout_view(request):
    logout(request)
    return redirect('/')

def user_update(request):
    if request.method == 'POST':
        user_form = UserUpdateForm(request.POST,instance=request.user)
        profile_form = ProfileUpdateForm(request.POST,instance=request.user.userprofile)


        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request,'Üye Bilgileriniz Güncellendi')
            return redirect('/user')
    else:
        category = Category.objects.all()
        user_form = UserUpdateForm(instance=request.user)
        profile_form = ProfileUpdateForm(instance=request.user.userprofile)
        return render(request,'user_update.html',{'category':category,'user_form':user_form,'profile_form':profile_form})



def product_details(request,id,slug):
    category = Category.objects.all()
    products = Product.objects.get(pk=id)

    return render(request,'product-details.html',{'category':category,'products':products})
