from django.urls import include, path
from . import views
from django.views.decorators.csrf import *
from django.conf import settings
from django.conf.urls.static import static
from product.views import *

urlpatterns=[
    path('',views.index,name='indexorder'),
    path('/addtocart/<int:id>',csrf_exempt(views.addtocart),name='addtocart'),
    path('/deletefromcart/<int:id>',views.deletefromcart,name='deletefromcart'),
    path('/shopcart', views.shopcart, name='shopcart'),
    path('/orderproduct',views.orderproduct,name='orderproduct')

]