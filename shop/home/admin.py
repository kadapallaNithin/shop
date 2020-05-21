from django.contrib import admin
from .models import Payment, Customer, Village, Product, Bill, Particular, Rate
# Register your models here.
admin.site.register(Payment)
admin.site.register(Customer)
admin.site.register(Village)
admin.site.register(Product)
admin.site.register(Bill)
admin.site.register(Particular)
admin.site.register(Rate)