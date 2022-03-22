"""soft re_path Configuration

The `re_pathpatterns` list routes re_paths to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/re_paths/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a re_path to re_pathpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a re_path to re_pathpatterns:  path('', Home.as_view(), name='home')
Including another re_pathconf
    1. Import the include() function: from django.re_paths import include, path
    2. Add a re_path to re_pathpatterns:  path('blog/', include('blog.re_paths'))
"""
from django.contrib import admin
from django.urls import include, path , re_path
from django.views.decorators.csrf import *
from product import views
from django.conf import settings
from django.conf.urls.static import static
from product.views import *
from order import views as orderviews

admin.site.site_title = "Ömer Aydemir"
admin.site.site_header = "Ömer Aydemir"


urlpatterns = [
    path('admin/', admin.site.urls),
    # re_path(r'^jet/', include('jet.re_paths', 'jet')),  # Django JET re_pathS
    # re_path(r'^jet/dashboard/', include('jet.dashboard.re_paths', 'jet-dashboard')),  # Django JET dashboard re_pathS
    re_path('^product/',include('product.urls')),
    re_path(r'^$',index,name='indexpage'),

    re_path(r'^log-in', log, name='log_in'),
    re_path(r'^logout', logout_view, name='logout'),
    re_path(r'^product-details', product_details, name='product_details'),

    path('ckeditor/', include('ckeditor_uploader.urls')),
    path('category/<int:id>/<slug:slug>',views.category_products,name='category'),
    path('product/<int:id>/<slug:slug>', views.product_details, name='product'),
    path('search/',views.product_search,name='product_search'),
    path('order', include('order.urls')),
    re_path(r'^order',views.order,name='order'),
    path('detail/<int:id>',views.order_detail,name='order-detail'),
    path('user',views.user_update,name='uye-update')
]  + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


