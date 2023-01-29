from django.contrib import admin


from product.models import Product, Comment, Favorites

admin.site.register(Product)
admin.site.register(Comment)


