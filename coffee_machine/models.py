from django.db import models

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
