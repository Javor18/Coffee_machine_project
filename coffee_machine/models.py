from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class CoffeMachine(models.Model):

    productName = models.CharField(max_length=100)
    # price_without_profit = models.IntegerField()
    # price_with_profit = models.IntegerField()
    price_with_profit = models.DecimalField(max_digits=5, decimal_places=2)
    # profit_percent = models.IntegerField()
    # image_itr = models.CharField(max_length=10)

    def __repr__(self):
        return self.productName, self.price_with_profit

# class CartItem(models.Model):
#
#     name = models.CharField(max_length=100)
#     price = models.DecimalField(max_digits=10, decimal_places=2)
#     quantity = models.IntegerField()
#     created_at = models.DateTimeField(auto_now_add=True)
#
#     def __repr__(self):
#         return self.name, self.price, self.quantity


class Cart(models.Model):

    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    drink_name = models.CharField(max_length=300)
    drink_price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
