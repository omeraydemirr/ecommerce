from django.contrib import admin
from .models import *
from mptt.admin import MPTTModelAdmin, DraggableMPTTAdmin
from django.utils.html import format_html

class ProductImageInline(admin.TabularInline):
    model = Images
    extra = 5

class CategoryAdmin(MPTTModelAdmin):
    list_display = ['title','status']
    list_filter = ['status']


class ProductAdmin(admin.ModelAdmin):
    list_display = ['title','category','price1','price2','amount','image_tag','status']
    readonly_fields = ('image_tag',)
    list_filter=['status','category']
    inlines = [ProductImageInline]

class ImagesAdmin(admin.ModelAdmin):
    list_display = ['title','product','image_tag']
    readonly_fields = ('image_tag',)

class MyDraggableMPTTAdmin(DraggableMPTTAdmin):
    list_display = ('tree_actions','something')
    list_display_links = ('something',)

    def something(self,instance):
        return format_html(
            '<div style="text-indent:{}px"{}</div>',
            instance._mpttfield('level') * self.mptt_level_indent,
            instance.title,
        )
    something.short_description= ('something_nice')

class CategoryAdmin2(DraggableMPTTAdmin):
    mptt_indent_field = "title"
    list_display = ('tree_actions', 'indented_title',
                    'related_products_count', 'related_products_cumulative_count')
    list_display_links = ('indented_title',)
    prepopulated_fields = {'slug':('title',)}

    def get_queryset(self, request):
        qs = super().get_queryset(request)

        # Add cumulative product count
        qs = Category.objects.add_related_count(
                qs,
                Product,
                'category',
                'products_cumulative_count',
                cumulative=True)

        # Add non cumulative product count
        qs = Category.objects.add_related_count(qs,
                 Product,
                 'category',
                 'products_count',
                 cumulative=False)
        return qs

    def related_products_count(self, instance):
        return instance.products_count
    related_products_count.short_description = 'Related Products (just for this category)'

    def related_products_cumulative_count(self, instance):
        return instance.products_cumulative_count
    related_products_cumulative_count.short_description = 'Related Products (for this and sub category)'

class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['user_name','phone','address','city']


admin.site.register(Category,CategoryAdmin2)
admin.site.register(Product,ProductAdmin)
admin.site.register(Images,ImagesAdmin)
admin.site.register(UserProfile)