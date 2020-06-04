from import_export import resources
from import_export.admin import ImportExportModelAdmin
from django.contrib import admin
from .models import Payment, Customer, Village, Product, Bill, Particular, Rate, Invoice
# Register your models here.
class VillageResource(resources.ModelResource):
    class Meta:
        model = Village
class VillageAdmin(ImportExportModelAdmin):
    resource_class = VillageResource
admin.site.register(Village, VillageAdmin)

class PaymentResource(resources.ModelResource):
    class Meta:
        model = Payment
class PaymentAdmin(ImportExportModelAdmin):
    resource_class = PaymentAdmin
admin.site.register(Payment)

class CustomerResouce(resources.ModelResource):
    class Meta:
        model = Customer
class CustomerAdmin(ImportExportModelAdmin):
    resource_class = CustomerResouce
admin.site.register(Customer, CustomerAdmin)

class ProductResource(resources.Resource):
    class Meta:
        model = Product
class ProductAdmin(ImportExportModelAdmin):
    resource_class = ProductResource
admin.site.register(Product, ProductResource)

class BillResouce(resources.Resource):
    class Meta:
        model = Bill
class BillAdmin(ImportExportModelAdmin):
    resource_class = BillResouce
admin.site.register(Bill, BillAdmin)


class ParticularResouce(resources.Resource):
    class Meta:
        model = Particular
class ParticularAdmin(ImportExportModelAdmin):
    resource_class = ParticularResouce
admin.site.register(Particular, ParticularAdmin)

class RateResouce(resources.Resource):
    class Meta:
        model = Rate
class RateAdmin(ImportExportModelAdmin):
    resource_class = RateResouce
admin.site.register(Rate, RateAdmin)

class InvoiceResouce(resources.Resource):
    class Meta:
        model = Invoice
class InvoiceAdmin(ImportExportModelAdmin):
    resource_class = InvoiceResouce
admin.site.register(Invoice, InvoiceAdmin)
