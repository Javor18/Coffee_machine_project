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

# ///////////////             /////////////////////



# class Customer(models.Model):
#     user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
#     name = models.CharField(max_length=200, null=True)
#     email = models.CharField(max_length=200, null=True)
#
#     def __str__(self):
#         return self.name
#
# class Product(models.Model):
#     name = models.CharField(max_length=200, null=True)
#     price = models.DecimalField(max_digits=7, decimal_places=2)
#     digital = models.BooleanField(default=False, null=True, blank=False)
#     image = models.ImageField(null=True, blank=True)
#
#     @property
#     def imageURL(self):
#         try:
#             url = self.image.url
#         except:
#             url = ''
#         return url
#
#     def __str__(self):
#         return self.name
#
# class Order(models.Model):
#     customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, blank=True, null=True)
#     date_ordered = models.DateTimeField(auto_now_add=True)
#     complete = models.BooleanField(default=False, null=True, blank=False)
#     transaction_id = models.CharField(max_length=200, null=True)
#
#     def __str__(self):
#         return str(self.id)
#
#     @property
#     def shipping(self):
#         shipping = False
#         orderitems = self.orderitem_set.all()
#         for i in orderitems:
#             if i.product.digital == False:
#                 shipping = True
#         return shipping
#
#     @property
#     def get_cart_total(self):
#         orderitems = self.orderitem_set.all()
#         total = sum([item.get_total for item in orderitems])
#         return total
#
#     @property
#     def get_cart_items(self):
#         orderitems = self.orderitem_set.all()
#         total = sum([item.quantity for item in orderitems])
#         return total


class CartItem(models.Model):

    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __repr__(self):
        return self.name, self.price, self.quantity
