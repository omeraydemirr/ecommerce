from django.contrib.auth.models import User
from django.db import models

# Create your models here.
from django.forms import ModelForm,TextInput
from product.models import Product

class ShopCart(models.Model):
    user = models.ForeignKey(User,verbose_name='Üye Adı',on_delete=models.SET_NULL,null=True)
    product = models.ForeignKey(Product,verbose_name='Ürün',on_delete=models.SET_NULL,null=True)
    quantity = models.IntegerField(verbose_name='Adet')


    def __str__(self):
        return self.product.title

    @property
    def amount(self):
        return int(self.quantity) * int(self.product.price2)

    @property
    def price(self):
        return (self.product.price2)


    class Meta:
        verbose_name = "Sepet"
        verbose_name_plural = "Sepettekiler"



class ShopCartForm(ModelForm):
    class Meta:
        model = ShopCart
        fields = ['quantity']


class Order(models.Model):
    STATUS = (
        ('Yeni','Yeni'),
        ('Sipariş Alındı', 'Sipariş Alındı'),
        ('Sipariş Hazırlanıyor', 'Sipariş Hazırlanıyor'),
        ('Sipariş Kargoda', 'Sipariş Kargoda'),
        ('Sipariş Tamamlandı', 'Sipariş Tamamlandı'),
        ('İptal Edildi', 'İptal Edildi'),
    )

    user = models.ForeignKey(User,verbose_name='Üye Adı',on_delete=models.SET_NULL,null=True)
    code = models.CharField(max_length=5,editable=False)
    first_name = models.CharField(verbose_name='Ad',max_length=10)
    last_name = models.CharField(verbose_name='Soyad',max_length=10)
    phone = models.CharField(verbose_name='Cep Telefonu',max_length=20,blank=False)
    address = models.CharField(verbose_name='Adres',blank=False,max_length=25)
    city = models.CharField(verbose_name='Şehir',blank=False,max_length=15)
    total = models.FloatField()
    status = models.CharField(verbose_name='Sipariş Durum',max_length=30,choices=STATUS,default='Yeni')
    ip = models.CharField(verbose_name='İp Adresi',blank=True,max_length=20)
    adminnote = models.CharField(verbose_name='Yönetici Notu',blank=True,max_length=100)
    create_at = models.DateTimeField(verbose_name='Eklenme Tarihi',auto_now_add=True)
    update_at = models.DateTimeField(verbose_name='Güncelleme Tarihi',auto_now=True)

    def __str__(self):
        if self.user is not None:
            return self.user.first_name
        else:
            return self.first_name

    class Meta:
        verbose_name = "Sipariş Raporu"
        verbose_name_plural = "Sipariş Raporları"


class OrderForm(ModelForm):
    class Meta:
        model = Order
        fields = ['first_name','last_name','address','phone','city']


class OrderProduct(models.Model):
    STATUS=(
        ('Yeni', 'Yeni'),
        ('Sipariş Alındı', 'Sipariş Alındı'),
        ('İptal Edildi', 'İptal Edildi'),
    )

    order = models.ForeignKey(Order,verbose_name='Sepet',on_delete=models.CASCADE)
    user = models.ForeignKey(User,verbose_name='Üye Adı',on_delete=models.CASCADE)
    product = models.ForeignKey(Product,verbose_name='Ürün',on_delete=models.CASCADE)
    quantity = models.IntegerField(verbose_name='Adet')
    price = models.FloatField(verbose_name='Fiyat')
    amount = models.FloatField(verbose_name='Toplam')
    status = models.CharField(verbose_name='Sipariş Durumu',max_length=30,choices=STATUS,default='Yeni')
    create_at = models.DateTimeField(verbose_name='Eklenme Tarihi',auto_now_add=True)
    update_at = models.DateTimeField(verbose_name='Güncelleme Tarihi',auto_now=True)

    def __str__(self):
        return self.product.title


    class Meta:
        verbose_name = "Sipariş"
        verbose_name_plural = "Siparişler"