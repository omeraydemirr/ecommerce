from django.contrib.auth.forms import UserChangeForm
from django.db import models
import os
# Create your models here.
from django.forms import ModelForm
from django.urls import reverse

from django.utils.safestring import mark_safe
from ckeditor_uploader.fields import RichTextUploadingField
from mptt.models import MPTTModel
from mptt.fields import TreeForeignKey
from django.contrib.auth.models import User

class Category(MPTTModel):
    STATUS=(
        (1,'YES'),
        (2,'NO'),
    )
    title = models.CharField(verbose_name='Category',max_length=150)
    keywords = models.CharField(verbose_name='Keywords',max_length=255,blank=True)
    description = models.CharField('Description',max_length=255,blank=True)
    image = models.ImageField()
    status = models.IntegerField(verbose_name='Stock',choices=STATUS)
    slug = models.SlugField()
    parent = TreeForeignKey('self',blank=True,null=True,related_name='children',on_delete=models.CASCADE)
    create_at = models.DateTimeField(verbose_name='Added Date',auto_now_add=True)
    update_at = models.DateTimeField(verbose_name='Updated Date',auto_now=True)
    
    class MPTTMeta:
        order_insertion_by = ['title']

    def __str__(self):
        full_path = [self.title]
        k = self.parent
        while k is not None:
            full_path.append(k.title)
            k = k.parent
        return  ' -> '.join(full_path[::-1])

    def image_tag(self):
        return mark_safe('<img src="{}" height="50"/>'.format(self.image.url))
    image_tag.short_description = 'Image'

    def get_absolute_url(self):
        return reverse('article_detail',kwargs={'slug':self.slug})

    class Meta:
        verbose_name = "Category"
        verbose_name_plural = "Categories"


class Product(models.Model):
    STATUS=(
        (1,'EVET'),
        (2,'HAYIR'),
    )
    category = models.ForeignKey(Category,verbose_name='Category',on_delete=models.CASCADE)
    title = models.CharField(verbose_name='Product Name',max_length=150)
    keywords = models.CharField(verbose_name='Keywords',max_length=255,blank=True)
    description = models.CharField(verbose_name='Description',max_length=255,blank=True)
    image = models.ImageField(verbose_name='Image')
    price1 = models.CharField(verbose_name='Price',max_length=120)
    price2 = models.CharField(verbose_name='Discounted Price',max_length=120,blank=True)
    amount = models.IntegerField(verbose_name='Total')
    detail=RichTextUploadingField(verbose_name='detail')
    slug = models.SlugField(verbose_name='Link',null=False,unique=True)
    status = models.IntegerField(verbose_name='Stock',choices=STATUS)
    create_at = models.DateTimeField(verbose_name='Added Date',auto_now_add=True)
    update_at = models.DateTimeField(verbose_name='Updated Date',auto_now=True)

    def __str__(self):
        return self.title


    def image_tag(self):
        return mark_safe('<img src="{}" height="50"/>'.format(self.image.url))
    image_tag.short_description= 'Image'
    def catimg_tag(self):
        return mark_safe((Category.status))
    catimg_tag.short_description = 'Small Image'

    class Meta:
        verbose_name = "Product"
        verbose_name_plural = "Products"

class Images(models.Model):
    product = models.ForeignKey(Product,on_delete=models.CASCADE)
    title = models.CharField(verbose_name='Product Name',max_length=50,blank=True)
    image = models.ImageField(verbose_name='Image',blank=True)




    def __str__(self):
        return self.title

    def image_tag(self):
        return mark_safe('<img src="{}" height="50"/>'.format(self.image.url))
    image_tag.short_description = 'Small Image'

    class Meta:
        verbose_name = "Image"
        verbose_name_plural = "Images"

class UserProfile(models.Model):
    user = models.OneToOneField(User,verbose_name='Member Name',on_delete=models.CASCADE)
    phone = models.CharField(verbose_name='Member Phone',blank=True,max_length=20)
    address = models.CharField(verbose_name='Member Address',blank=True,max_length=150)
    city = models.CharField(verbose_name='Member City',blank=True,max_length=20)

    def __str__(self):
        return self.user.username

    def user_name(self):
        return self.user.first_name + ' ' + self.user.first_name + ' [' +self.user.username + '] '


    class Meta:
        verbose_name = "User Profile"
        verbose_name_plural = "User Profiles"

class UserProfileForm(ModelForm):
    class Meta:
        model = UserProfile
        fields = ['phone','address','city']


