from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class Category(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

class Product(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    prise = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.ForeignKey(Category, null=True, blank=True, on_delete=models.SET_NULL)

    def __str__(self):
        return self.name


class Review(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reviews')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='reviews')
    content = models.TextField()
    rating = models.PositiveIntegerField()
    date_posted = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.product.name} - {self.rating}"


class FlashSale(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE) #bu product bilan bog'lanadi
    discount_percentage = models.PositiveIntegerField() # bu qancha chegirmani ifodalydi
    start_time = models.DateTimeField()# bu chegirmani boshlanish vaqti
    end_time = models.DateTimeField()# bu chegirmani tugash vaqti

    def is_active(self):# bu active yoki emasligini qaytaradi
        now = timezone.now()# hozirgi vaqt
        return self.start_time <= now <= self.end_time # true yoki False qaytaradi

    class Meta:
        unique_together = ('product', 'start_time', 'end_time') # bu 1 ta maxsulotga ko'p chegirma berishni oldini oladi
# bu menga produktni ko'rib unga qiziqanlar ro'yxatini ko'rsatadi
class ProductViewHistory(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)
