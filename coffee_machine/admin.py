from django.contrib import admin
from coffee_machine.models import CoffeMachine

class CoffeMachineAdmin(admin.ModelAdmin):
    list_display = ('productName', 'price_with_profit')
admin.site.register(CoffeMachine, CoffeMachineAdmin)


