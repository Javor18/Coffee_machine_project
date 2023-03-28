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

    def __str__(self):
        return self.productName

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


class Customer(models.Model):

    user = models.OneToOneField(User, null=True, blank=True, on_delete=models.CASCADE)
    name = models.CharField(max_length=200, null=True)
    email = models.CharField(max_length=200)

    def __str__(self):
        return self.name


class Order(models.Model):

        customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, blank=True, null=True)
        date_ordered = models.DateTimeField(auto_now_add=True)
        complete = models.BooleanField(default=False)
        transaction_id = models.CharField(max_length=100, null=True)

        def __str__(self):
            return str(self.id)

        @property
        def get_cart_total(self):
            orderitems = self.orderitem_set.all()
            total = sum([item.get_total for item in orderitems])
            return total

        @property
        def get_cart_items(self):
            orderitems = self.orderitem_set.all()
            total = sum([item.quantity for item in orderitems])
            return total

class OrderItem(models.Model):

        product = models.ForeignKey(CoffeMachine, on_delete=models.SET_NULL, null=True)
        order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True)
        quantity = models.IntegerField(default=0, null=True, blank=True)
        date_added = models.DateTimeField(auto_now_add=True)


        @property
        def get_total(self):
            total = self.product.price_with_profit * self.quantity
            return total

