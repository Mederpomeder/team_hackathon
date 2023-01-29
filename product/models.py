from ckeditor.fields import RichTextField
from django.contrib.auth import get_user_model
from django.db import models
from django.contrib.auth import get_user_model
from django.db import models
# from category.models import Category
from ckeditor.fields import RichTextField

User = get_user_model()


from category.models import Category

User = get_user_model()


class Product(models.Model):
    STATUS_CHOICES = (
        ('in_stock', 'Свободно'),
        ('out_of_stock', 'Несвободно')
    )
    owner = models.ForeignKey(User, on_delete=models.RESTRICT, related_name='products')
    title = models.CharField(max_length=150)
    description = RichTextField()
    category = models.ForeignKey(Category, related_name='products', on_delete=models.RESTRICT)
    preview = models.ImageField(upload_to='images', null=True)
    price = models.DecimalField(max_digits=12, decimal_places=2)
    stock = models.CharField(choices=STATUS_CHOICES, max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class Comment(models.Model):
    owner = models.ForeignKey(User, related_name='comments', on_delete=models.CASCADE)
    post = models.ForeignKey(Product, related_name='comments', on_delete=models.CASCADE)
    body = models.TextField(max_length=505)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.owner} -> {self.post} -> {self.created_at}'


class Like(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='liked_posts')
    post = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='likes')

    class Meta:
        unique_together = ['owner', 'post']


class PostImages(models.Model):
    title = models.CharField(max_length=100, blank=True)
    image = models.ImageField(upload_to='images/')
    post = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='images')

    def generate_name(self):
        from random import randint
        return 'image' + str(self.id) + str(randint(100000, 1_000_000))

    def save(self, *args, **kwargs):
        self.title = self.generate_name()
        return super(PostImages, self).save(*args, **kwargs)


class Favorites(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='favorites')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='favorites')

    class Meta:
        unique_together = ['owner', 'product']

