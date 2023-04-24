from django.contrib import admin
from coffee_machine.models import *

class CoffeMachineAdmin(admin.ModelAdmin):
    list_display = ('productName', 'price_with_profit')
admin.site.register(CoffeMachine, CoffeMachineAdmin)

# admin.site.register(Customer)
admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(Cart)

