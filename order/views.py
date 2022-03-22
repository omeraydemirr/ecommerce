from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse,HttpResponseRedirect
from django.shortcuts import render
from django.utils.crypto import get_random_string

from order.models import ShopCartForm, ShopCart, OrderForm, Order, OrderProduct
from product.models import Category, Product, UserProfile


def index(request):
    return HttpResponse("Order App")

def addtocart(request,id):
    url = request.META.get('HTTP_REFERER') #get Last url
    current_user = request.user #Access USer Session information
    #***************IF THERE IS PRODUCT ON CART****************"
    checkproduct = ShopCart.objects.filter(product_id=id)

    if checkproduct:
        control = 1 #There is product
    else:
        control = 0 #There is no product


    if request.method == 'POST':
        form = ShopCartForm(request.POST)
        if form.is_valid():
            if control == 1: #Update if product exists
                data = ShopCart.objects.get(product_id=id)
                data.quantity += form.cleaned_data['quantity']
                data.save()
            else: #Add if no product
                data = ShopCart()
                data.user_id = current_user.id
                data.product_id = id
                data.quantity = form.cleaned_data['quantity']
                data.save()
        request.session['cart_items'] = ShopCart.objects.filter(user_id=current_user.id).count()
        messages.success(request,"Ürün Başarı ile Sepete Eklenmiştir")
        return HttpResponseRedirect(url)

    else: #If directly clicked  'add cart' button
        if control == 1:
            data = ShopCart.objects.get(product_id=id)
            data.quantity += 1
            data.save()
        else:
            data = ShopCart()
            data.user_id = current_user.id
            data.product_id = id
            data.quantity = 1
            data.save()
        request.session['cart_items'] = ShopCart.objects.filter(user_id=current_user.id).count()
        messages.success(request, "Ürün Başarı ile Sepete Eklenmiştir")
        return HttpResponseRedirect(url)

    messages.warning(request,"Ürün eklemede hata oluştu!")
    return HttpResponseRedirect(url)

def shopcart(request):
    category = Category.objects.all()
    current_user = request.user
    request.session['cart_items'] = ShopCart.objects.filter(user_id=current_user.id).count()
    schopcart = ShopCart.objects.filter(user_id=current_user.id)
    total = 0
    for rs in schopcart:
        total += int(rs.product.price2) * int(rs.quantity)
    return render(request,'cart.html',{'schopcart':schopcart,'category':category,'total':total})



def deletefromcart(request,id):
    ShopCart.objects.filter(id=id).delete()
    messages.success(request,"Ürün Sepetten Silinmiştir")
    return HttpResponseRedirect("/order/shopcart")


def orderproduct(request):
    category = Category.objects.all()
    current_user = request.user
    schopcart = ShopCart.objects.filter(user_id=current_user.id)
    total = 0
    for rs in schopcart:
        total += int(rs.product.price2) * int(rs.quantity)

    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            data = Order()
            data.first_name = form.cleaned_data['first_name']
            data.last_name = form.cleaned_data['last_name']
            data.address = form.cleaned_data['address']
            data.city = form.cleaned_data['city']
            data.phone = form.cleaned_data['phone']
            data.user_id = current_user.id
            data.total = total
            data.ip = request.META.get('REMOTE_ADDR')
            ordercode = get_random_string(5).upper()
            data.code = ordercode
            data.save()
            #Move shopcart items to order products item
            schopcart = ShopCart.objects.filter(user_id=current_user.id)
            for rs in schopcart:
                detail = OrderProduct()
                detail.order_id = data.id
                detail.product_id = rs.product.id
                detail.user_id = current_user.id
                detail.quantity = rs.quantity
                #Reduce quantity of sold product from Amount of Product
                product = PRODUCT.objects.get(id=rs.product.id)
                product.amount -= rs.quantity
                product.save()

                detail.price = ((rs.product.price2) or (rs.product.price1))
                detail.amount = rs.amount
                detail.save()

            ShopCart.objects.filter(user_id=current_user.id).delete() #Clear & Delete shopcart
            request.session['cart_items'] = 0
            messages.success(request,"Siparişiniz Alınmıştır.Teşekkür Ederiz")
            #return render(request,'',{'ordercode':ordercode,'category':category})
            return HttpResponseRedirect('/',{"ordercode":ordercode,'category':category})
        else:
            messages.warning(request,form.errors)
            return HttpResponseRedirect("/order/orderproduct")

    form = OrderForm()
    profile = UserProfile.objects.get(user_id=current_user.id)
    return render(request,'checkout.html',{'schopcart':schopcart,'category':category,'total':total,'form':form,'profile':profile})


















