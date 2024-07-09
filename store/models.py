from django.db import models

from django.urls import reverse

# Create your models here.

class Size(models.Model):
    name = models.CharField(max_length=50, unique=True)

    class Meta:

        verbose_name_plural = 'size'

    def __str__(self):
        return self.name

class Category(models.Model):

    name = models.CharField(max_length=255, db_index=True)

    slug = models.SlugField(max_length=255, unique=True)

    class Meta:

        verbose_name_plural = 'categories'

    def __str__(self):
        return self.name
    

    def get_absolute_url(self):

        return reverse('list-category', args=[self.slug])


class Product(models.Model):

    category = models.ForeignKey(Category, related_name='product', on_delete=models.CASCADE, null=True)

    sizes = models.ManyToManyField(Size, related_name='products')

    title = models.CharField(max_length=255)

    brand = models.CharField(max_length=255, default='un-branded')

    description = models.TextField(blank=True)

    slug = models.SlugField(max_length=255)

    price = models.DecimalField(max_digits=10, decimal_places=3)

    image = models.ImageField(upload_to='images/')

    status = models.CharField(max_length=255, default='Còn hàng')


    class Meta:

        verbose_name_plural = 'products'

    def __str__(self):
        return self.title


    def get_absolute_url(self):

        return reverse('product-info', args=[self.slug])


class DailyMetrics(models.Model):
    date = models.DateField(auto_now_add=True)
    money = models.DecimalField(max_digits=10, decimal_places=2)
    users = models.IntegerField()
    new_clients = models.IntegerField()
    sales = models.DecimalField(max_digits=10, decimal_places=2)
    website_views = models.IntegerField()
    daily_sales = models.DecimalField(max_digits=10, decimal_places=2)
    completed_tasks = models.IntegerField()

    def __str__(self):
        return f"Metrics for {self.date}"